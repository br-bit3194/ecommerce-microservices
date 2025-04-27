from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import IntegrityError


from .models import Products, Category
from .serializers import ProductSerializer, CategorySerializer
from .utils import parse_serializer_errors

# Create your views here.
@api_view(["GET"])
def health_check(request):
    return JsonResponse({"status": "healthy"})

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(APIView):
    def get(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        print(correlation_id)
        # Logic to retrieve categories
        try:
            all_categories = Category.objects.all()
            serialized_categories = CategorySerializer(all_categories, many=True).data
            return JsonResponse({"data": serialized_categories}, status=status.HTTP_200_OK)
        except Exception as e:
            # Custom error handling in case something goes wrong
            # logger.error(f"Error fetching categories: {str(e)}", exc_info=True)
            return JsonResponse(
                {"error": "Failed to retrieve categories. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        print(correlation_id)
        # Logic to create a new category
        category_data = request.data
        serializer = CategorySerializer(data=category_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return JsonResponse({"data": serializer.data}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                # In case model-level unique constraint throws an error
                return JsonResponse({"error": "Category already exists"}, status=status.HTTP_400_BAD_REQUEST)

        parsed_errors = parse_serializer_errors(serializer.errors)
        err_resp = {"errors": parsed_errors}
        return JsonResponse(err_resp, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class ProductsView(APIView):
    def get(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        print(correlation_id)
        # Logic to retrieve products
        try:
            # Logic to retrieve all products
            all_products = Products.objects.all()
            serialized_products = ProductSerializer(all_products, many=True).data

            # logger.info(f"Successfully retrieved {len(all_products)} products.")

            # Return success response with serialized product data
            return JsonResponse({"data": serialized_products}, status=status.HTTP_200_OK)

        except Exception as e:
            # Log unexpected errors
            # logger.error(f"Error occurred while retrieving products (Correlation ID: {correlation_id}): {str(e)}",
            #              exc_info=True)
            # Return generic error message for unexpected issues
            return JsonResponse(
                {"error": "An unexpected error occurred while retrieving products. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        print(correlation_id)
        # Logic to create a new product
        product_data = request.data
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"data": serializer.data}, status=status.HTTP_201_CREATED)

        parsed_errors = parse_serializer_errors(serializer.errors)
        err_resp = {"errors": parsed_errors}
        return JsonResponse(err_resp, status=status.HTTP_400_BAD_REQUEST)