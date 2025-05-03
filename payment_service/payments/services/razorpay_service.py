import razorpay
import logging
from django.conf import settings
# from razorpay.errors import BadRequestError

from ..interfaces.payment_gateway import IPaymentGateway
from ..constants.razorpay_constants import ORDER_CURRENCY
from ..models import Payment
from ..enums import PaymentStatus

logger = logging.getLogger(__name__)


class RazorpayService(IPaymentGateway):
    def __init__(self, razorpay_key_id, razorpay_key_secret):
        self.client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))

    def create_order(self, order_id: int, amount: int, receipt: str) -> dict:
        '''
        this will be used with razorpay to create an order then checkout page (if we have custom checkout page)
        '''
        try:
            # Validate amount
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            # Validate receipt
            if not isinstance(receipt, str) or not receipt.strip():
                raise ValueError("Receipt must be a non-empty string.")

            razorpay_order = self.client.order.create({
                "amount": amount * 100,
                "currency": ORDER_CURRENCY,
                "receipt": receipt
            })

            payment_obj = Payment.objects.create(order_id = order_id,
                                    razorpay_order_id = razorpay_order['id'],
                                    amount = amount,
                                    currency = ORDER_CURRENCY,
                                    status = PaymentStatus.PENDING.value,
                                    receipt = receipt)

            payment_obj.save()
            return {
                "id": payment_obj.id,
                "razorpay_order_id": razorpay_order['id'],
                "amount": amount,
                "currency": ORDER_CURRENCY,
                "receipt": receipt
            }
        # except BadRequestError:
        #     error = e['error']
        #     print(error)
        #     raise Exception(f"Razorpay error: {error['description']}")
        except Exception as e:
            print(e)
            raise Exception(f"An error occurred while creating the order: {str(e)}")

    def create_payment_link(self, request_id: str, order_id: int, amount: int, name: str, email: str, callback_url=None) -> dict:
        '''
        this will be used with razorpay to create a payment link
        '''
        try:
            logger.info(f"Creating payment link for order_id: {order_id}, amount: {amount}, name: {name}, email: {email}", extra={"correlation_id": request_id})
            # Validate amount
            if amount <= 0:
                logger.error(f"Invalid amount: {amount}", extra={"correlation_id": request_id})
                raise ValueError("Amount must be greater than zero.")

            # Validate name
            if not isinstance(name, str) or not name.strip():
                logger.error(f"Invalid name: {name}", extra={"correlation_id": request_id})
                raise ValueError("Name must be a non-empty string.")

            # Validate email
            if not isinstance(email, str) or not email.strip():
                logger.error(f"Invalid email: {email}", extra={"correlation_id": request_id})
                raise ValueError("Email must be a non-empty string.")

            callback_url = settings.PAYMENT_LINK_CALLBACK_URL if callback_url is None else callback_url

            data = {
                "amount": amount * 100,
                "currency": ORDER_CURRENCY,
                "description": f"Payment for Order {order_id}",
                "accept_partial": False,
                "reminder_enable": False,
                "reference_id": str(request_id),
                "notes": {
                    "order_id": order_id,
                    "name": name,
                    "email": email,
                    "request_id": request_id
                },
                "notify": {
                    "sms": False,
                    "email": True  # ✅ send email notification
                },
                "callback_url": callback_url
            }

            payment_link = self.client.payment_link.create(data=data)
            logger.info(f"Payment link created: {payment_link}", extra={"correlation_id": request_id})

            # store in payment table
            payment_obj = Payment.objects.create(order_id = order_id,
                                    razorpay_payment_link_id = payment_link['id'],
                                    razorpay_short_url = payment_link['short_url'],
                                    amount = amount,
                                    currency = ORDER_CURRENCY,
                                    status = PaymentStatus.PENDING.value,
                                    receipt = f"order_{order_id}")
            payment_obj.save()
            logger.info(f"Payment object created with id: {payment_obj.id}", extra={"correlation_id": request_id})

            payment_link.update({"payment_id": payment_obj.id})
            return payment_link

        # except BadRequestError as e:
        #     error = e['error']
        #     print(error)
        #     raise Exception(f"Razorpay error: {error['description']}")
        except Exception as e:
            logger.exception(f"Error creating payment link: {str(e)}", extra={"correlation_id": request_id})
            raise Exception(f"An error occurred while creating the payment link: {str(e)}")

    def verify_payment_link_signature(self, request_id: str, razorpay_payment_id: str, razorpay_payment_link_id: str,
                         razorpay_signature: str):
        try:
            self.client.utility.verify_payment_link_signature({
                "razorpay_payment_link_id": razorpay_payment_link_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })
            logger.info(f"Signature verified successfully", extra={"correlation_id": request_id})
            return True
        except Exception as e:
            logger.error(f"Signature verification failed: {str(e)}", extra={"correlation_id": request_id})
            return False