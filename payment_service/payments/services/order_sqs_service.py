import boto3
import json
from django.conf import settings

def send_order_status_update(request_id, order_id, payment_id, payment_status):
    sqs = boto3.client('sqs', region_name=settings.AWS_REGION)

    payload = {
        "source": "payment_service",
        "order_id": order_id,
        "payment_id": payment_id,
        "payment_status": payment_status,
        "correlation_id": request_id,
    }

    response = sqs.send_message(
        QueueUrl=settings.ORDER_UPDATE_QUEUE_URL,
        MessageBody=json.dumps(payload)
    )
    return response
