import logging
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import Users

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(["POST"])
def register(request):
    correlation_id = request.correlation_id
    try:
        logger.info("User registration started", extra={"correlation_id": correlation_id})
        data = request.data
        user = UserSerializer(data=data)
        if user.is_valid():
            user.save()
            logger.info("User registration completed", extra={"correlation_id": correlation_id})
            return Response(user.data, status=status.HTTP_201_CREATED)

        logger.error(f"User registration failed: {user.errors}", extra={"correlation_id": correlation_id})
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.exception(f"Error during user registration: {str(e)}", extra={"correlation_id": correlation_id})
        return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def get_user_details(request, user_id):
    correlation_id = request.correlation_id
    try:
        logger.info(f"Fetching user details for user_id: {user_id}", extra={"correlation_id": correlation_id})
        data = Users.objects.get(id=user_id)
        serialized_user = UserSerializer(data).data
        logger.info(f"Fetched user details successfully for user_id: {user_id}", extra={"correlation_id": correlation_id})
        return Response(serialized_user, status=status.HTTP_200_OK)
    except Users.DoesNotExist:
        logger.error(f"User not found for user_id: {user_id}", extra={"correlation_id": correlation_id})
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(f"Error fetching user details: {str(e)}", extra={"correlation_id": correlation_id})
        return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)