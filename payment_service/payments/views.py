import logging
from rest_framework.decorators import api_view
from django.http import JsonResponse

from django.conf import settings
from .services.razorpay_service import RazorpayService
from .enums import PaymentStatus
from .models import Payment
from .services.order_sqs_service import send_order_status_update

razorpay_service = RazorpayService(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)

logger = logging.getLogger(__name__)

@api_view(["POST"])
def create_payment_link(request):
    """
    Create a payment link.
    """
    request_id = request.correlation_id  # Get correlation id from middleware
    # Extract data from request
    order_id = request.data.get("order_id")
    amount = int(request.data.get("amount"))
    name = request.data.get("name")
    email = request.data.get("email")

    # Validate input
    if not order_id or not amount or not name or not email:
        return JsonResponse({"error": "Missing required fields."}, status=400)

    # Create payment link using Razorpay service

    callback_url = settings.PAYMENT_LINK_CALLBACK_URL
    try:
        payment_link = razorpay_service.create_payment_link(request_id, order_id, amount, name, email, callback_url)
        return JsonResponse(payment_link, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(["GET"])
def payment_link_callback(request):
    """
    Handle payment link callback.
    """
    request_id = request.GET.get("razorpay_payment_link_reference_id")
    try:
        logger.info(f"Payment link callback received with Request data: {request.GET}", extra={"correlation_id": request_id})

        # Extract data from request
        razorpay_payment_id = request.GET.get("razorpay_payment_id")
        razorpay_payment_link_id = request.GET.get("razorpay_payment_link_id")
        # razorpay_payment_link_reference_id -> request_id/correlation_id
        # razorpay_payment_link_reference_id = request.GET.get("razorpay_payment_link_reference_id")
        razorpay_payment_link_status = request.GET.get("razorpay_payment_link_status")
        razorpay_signature = request.GET.get("razorpay_signature")

        # request_id = razorpay_payment_link_reference_id

        logger.info(f"Payment link callback received with payment ID: {razorpay_payment_id}, payment link ID: {razorpay_payment_link_id}, status: {razorpay_payment_link_status}", extra={"correlation_id": request_id})
        logger.info(f"Payment link callback received with signature: {razorpay_signature}", extra={"correlation_id": request_id})

        # Validate input
        if not razorpay_payment_id or not razorpay_payment_link_id or not razorpay_payment_link_status:
            logger.error(f"Missing required fields for payment link callback: {request.data}", extra={"correlation_id": request_id})
            return JsonResponse({"error": "Missing required fields."}, status=400)

        # Validate signature
        if not razorpay_service.verify_payment_link_signature(request_id, razorpay_payment_id, razorpay_payment_link_id, razorpay_signature):
            logger.error(f"Invalid signature for payment link ID: {razorpay_payment_link_id}", extra={"correlation_id": request_id})
            return JsonResponse({"error": "Invalid signature."}, status=400)


        # get payment object
        payment_obj = Payment.objects.get(razorpay_payment_link_id=razorpay_payment_link_id)
        if not payment_obj:
            logger.error(f"Payment object not found for payment link ID: {razorpay_payment_link_id}", extra={"correlation_id": request_id})
            return JsonResponse({"error": "Payment object not found."}, status=400)

        logger.info(f"Payment object found: {payment_obj}", extra={"correlation_id": request_id})

        payment_status = razorpay_payment_link_status
        reason = None
        if razorpay_payment_link_status == PaymentStatus.PAID.value:
            # Update payment status in the database
            payment_status = PaymentStatus.COMPLETED.value
        else:
            # Update payment status in the database
            reason = f"Payment {payment_status}"
            payment_status = PaymentStatus.FAILED.value

        # Update razorpay_payment_id in the database
        payment_obj.status = payment_status
        payment_obj.razorpay_payment_id = razorpay_payment_id
        payment_obj.reason = reason
        payment_obj.save()

        # fetch order id from payment object
        order_id = payment_obj.order_id
        payment_id = payment_obj.id

        logger.info(
            f"Payment link callback processed successfully for payment link ID: {razorpay_payment_link_id} with payment_status: {payment_status}",
            extra={"correlation_id": request_id})

        # Send order status update to SQS
        send_order_status_update(request_id, order_id, payment_id, payment_status)

        logger.info(f"Order status update sent to SQS for order ID: {order_id} with payment status: {payment_status} & payment_id: {payment_id}", extra={"correlation_id": request_id})

        return JsonResponse({"status": "success"}, status=200)
    except Exception as e:
        logger.exception(f"Error processing payment link callback: {str(e)}", extra={"correlation_id": request_id})
        return JsonResponse({"error": str(e)}, status=500)