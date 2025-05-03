import boto3
import json
from django.conf import settings

def send_payment_init_message(request_id, order_id, amount, customer_name, customer_email):
    sqs = boto3.client('sqs', region_name=settings.AWS_REGION)

    payload = {
        "source": "order_service",
        "order_id": order_id,
        "amount": amount,
        "name": customer_name,
        "email": customer_email,
        "correlation_id": request_id,
    }

    response = sqs.send_message(
        QueueUrl=settings.PAYMENT_UPDATE_QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
    return response
