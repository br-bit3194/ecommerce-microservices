import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .enums import OrderStatus
from .models import Order
from .serializers import OrderSerializer
from .services.order_manager import OrderManager

logger = logging.getLogger(__name__)

PRODUCT_SERVICE_URL = "http://localhost:8001/products/check_stock/"

# Create your views here.
class OrderView(APIView):
    def get(self, request):
        # Logic to retrieve orders
        correlation_id = request.correlation_id
        try:
            logger.info("Retrieving orders", extra={'correlation_id': correlation_id})
            serializer = OrderManager.list_all_orders(correlation_id)
            logger.info(f"Orders retrieved successfully: {len(serializer.data)} orders", extra={'correlation_id': correlation_id})
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the error with the correlation ID
            logging.exception(f"Error retrieving orders: {e}", extra={'correlation_id': correlation_id})
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        # Logic to create a new order
        correlation_id = request.correlation_id
        try:
            logger.info("Creating order", extra={'correlation_id': correlation_id})
            data = request.data
            user_id = data.get('user_id')
            items = data.get('items')  # [{product_id: 1, quantity: 2}, ...]

            if not items:
                return Response({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)
            if not user_id:
                return Response({"error": "No user_id provided"}, status=status.HTTP_400_BAD_REQUEST)

            # create order
            order_obj, error = OrderManager.create_order(correlation_id, data)
            if error:
                logger.error("Order creation failed", extra={'correlation_id': correlation_id})
                return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

            #

            # Serialize the order object
            serializer = OrderSerializer(order_obj)
            logger.info("Order created successfully", extra={'correlation_id': correlation_id})
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Log the error with the correlation ID
            logging.exception(f"Error creating order: {e}", extra={'correlation_id': correlation_id})
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)