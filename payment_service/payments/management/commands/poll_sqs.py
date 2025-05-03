import boto3
import logging
import requests
import json
from django.core.management.base import BaseCommand

from payments.models import Payment
from payments.enums import PaymentStatus
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Poll AWS SQS for new payment initiation request'

    def handle(self, *args, **kwargs):
        sqs = boto3.client('sqs', region_name=settings.AWS_REGION)
        queue_url = settings.PAYMENT_UPDATE_QUEUE_URL if settings.PAYMENT_UPDATE_QUEUE_URL else "payment-update-queue"  # SQS queue URL
        payment_service_base_url = settings.PAYMENT_SERVICE_BASE_URL if settings.PAYMENT_SERVICE_BASE_URL else "http://localhost:8003"  # Base URL for payment service

        while True:
            logger.info("Polling SQS for new payment initiation request...")
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20  # long polling
            ).get('Messages', [])

            logger.info(f"Received {len(messages)} messages from SQS")
            for msg in messages:
                body = json.loads(msg['Body'])
                try:
                    # "source": "order_service",
                    # "order_id": order_id,
                    # "amount": amount,
                    # "name": customer_name,
                    # "email": customer_email,
                    # "correlation_id": request_id,

                    # Check if the message is from the correct source
                    if body.get('source') != 'order_service':
                        logger.error(f"Ignoring message from unknown source: {body.get('source')}")
                        continue

                    request_id = body.get('correlation_id')
                    order_id = body.get('order_id')

                    # create payment link using Razorpay service
                    data = {"order_id": order_id,
                            "amount": body.get('amount'),
                            "name": body.get('name'),
                            "email": body.get('email')}

                    # hit payment service to create payment link
                    requests.post(f"{payment_service_base_url}/create_payment_link/", json=data, headers={"X-Correlation-ID": request_id})

                    logger.info(f"Payment link created for order {order_id}", extra={"correlation_id": request_id})

                    # delete message from queue
                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=msg['ReceiptHandle']
                    )

                    logger.info(f"Deleted message from SQS", extra={"correlation_id": request_id})

                except Exception as e:
                    logger.exception(f"Failed to process message: {e}", extra={"correlation_id": body.get('correlation_id')})
