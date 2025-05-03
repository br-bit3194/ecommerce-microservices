import boto3
import logging
import json
from django.core.management.base import BaseCommand

from orders.models import Order
from orders.services.order_manager import OrderManager
from orders.enums import OrderStatus
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Poll AWS SQS for update order status'

    def handle(self, *args, **kwargs):
        sqs = boto3.client('sqs', region_name=settings.AWS_REGION)
        queue_url = settings.ORDER_UPDATE_QUEUE_URL if settings.ORDER_UPDATE_QUEUE_URL else "order-update-queue"  # SQS queue URL

        while True:
            logger.info("Polling SQS for order status update from payment...")
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20  # long polling
            ).get('Messages', [])

            logger.info(f"Received {len(messages)} messages from SQS")
            for msg in messages:
                body = json.loads(msg['Body'])
                try:
                    # "source": "payment_service",
                    # "order_id": order_id,
                    # "payment_id": payment_id,
                    # "payment_status": payment_status,
                    # "correlation_id": request_id,

                    # Check if the message is from the correct source
                    if body.get('source') != 'payment_service':
                        logger.error(f"Ignoring message from unknown source: {body.get('source')}")
                        continue

                    request_id = body.get('correlation_id')
                    order_id = body.get('order_id')
                    payment_status = body.get('payment_status')

                    # update order status in the database
                    data = {"status": payment_status}
                    OrderManager.update_order_by_id(request_id, order_id, data)

                    logger.info(f"Order {order_id} updated with status {payment_status}", extra={"correlation_id": request_id})

                    # delete message from queue
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=msg['ReceiptHandle']
                    )

                    logger.info(f"Deleted message from SQS", extra={"correlation_id": request_id})

                except Exception as e:
                    logger.exception(f"Failed to process message: {e}", extra={"correlation_id": body.get('correlation_id')})
