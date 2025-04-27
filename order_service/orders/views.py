import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .enums import OrderStatus
from .models import Order
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)

# Create your views here.
class OrderView(APIView):
    def get(self, request):
        # Logic to retrieve orders
        correlation_id = request.correlation_id
        try:
            logger.info("Retrieving orders", extra={'correlation_id': correlation_id})
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            logger.info(f"Orders retrieved successfully: {len(orders)} orders", extra={'correlation_id': correlation_id})
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
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                order = serializer.save()
                logger.info(f"Order created successfully: {order.id}", extra={'correlation_id': correlation_id})
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

            logger.error("Order creation failed", extra={'correlation_id': correlation_id})
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the error with the correlation ID
            logging.exception(f"Error creating order: {e}", extra={'correlation_id': correlation_id})
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)