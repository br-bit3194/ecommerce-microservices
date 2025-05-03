import logging
import requests, json
from Tools.scripts.generate_opcode_h import header
from django.conf import settings
from rest_framework import status

from ..models import Order, OrderItems
from ..serializers import OrderSerializer
from ..enums import OrderStatus
from ..services.payment_sqs_service import send_payment_init_message

logger = logging.getLogger(__name__)

PRODUCT_SERVICE_URL = settings.PRODUCT_SERVICE_URL
USER_SERVICE_URL = settings.USER_SERVICE_URL

class OrderManager:

    @staticmethod
    def list_all_orders(request_id):
        order_objs = Order.objects.all()
        return OrderSerializer(order_objs, many=True)

    @staticmethod
    def get_order_by_id(request_id, order_id):
        order_obj = Order.objects.get(id=order_id)
        return OrderSerializer(order_obj)

    @staticmethod
    def update_order_by_id(request_id, order_id, data):
        Order.objects.filter(id=order_id).update(**data)
        return

    @staticmethod
    def check_product_stock(request_id, items):
        data = {
            "items": items
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Correlation-ID': request_id
        }
        product_response = requests.post(f"{PRODUCT_SERVICE_URL}/check_stock/", json=data, headers=headers)
        if product_response.status_code != status.HTTP_200_OK:
            logger.error(f"[{request_id}]: {product_response.text}")
            return False

        logger.info(f"[{request_id}]: All products are available")
        return True

    @staticmethod
    def get_user_details_by_id(request_id, user_id):
        headers = {
            'Content-Type': 'application/json',
            'X-Correlation-ID': request_id
        }
        user_response = requests.get(f"{USER_SERVICE_URL}/{user_id}/", headers=headers)
        if user_response.status_code != status.HTTP_200_OK:
            logger.error(f"[{request_id}]: {user_response.text}")
            return {}

        logger.info(f"User details fetched successfully", extra={"correlation_id": request_id})
        return user_response.json()

    @staticmethod
    def create_order(request_id, data):
        user_id = data.get('user_id')
        items = data.get('items')  # [{product_id: 1, quantity: 2}, ...]

        # Step 1: Check if products are available
        is_products_available = OrderManager.check_product_stock(request_id, items)

        if not is_products_available:
            return None, {"error": f"Products unavailable"}

        # Step 1.1: Get user details
        user_details = OrderManager.get_user_details_by_id(request_id, user_id)

        # Step 2: Calculate the total price of the order
        total_price = 0
        for item in items:
            price = item['price']
            quantity = item['quantity']
            total_price += price * quantity

        logger.info(f"Total price calculated: {total_price}", extra={"correlation_id": request_id})

        # Step 3: Create the order
        order_data = {
            'user_id': user_id,
            'total_price': total_price,
            'status': OrderStatus.PENDING.value  # Default status when order is created
        }

        order = Order.objects.create(**order_data)

        # Step 4: Create order items
        for item in items:
            OrderItems.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )

        logger.info(f"Order created with ID: {order.id}", extra={"correlation_id": request_id})

        # Step 5: Notify payment service (to be handled after order creation)
        order_id = order.id
        amount = order.total_price
        customer_name = user_details.get('name')
        customer_email = user_details.get('email')

        send_payment_init_message(request_id, order_id, amount, customer_name, customer_email)

        # Step 5: Update product stock (to be handled after order creation)

        # OrderManager.update_product_stock(items)

        return order, None