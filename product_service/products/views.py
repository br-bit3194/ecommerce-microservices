# products/views.py
import logging
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Products
from .services.product_manager import ProductManager
from .services.category_manager import CategoryManager

logger = logging.getLogger(__name__)


@api_view(["GET"])
def health_check(request):
    return JsonResponse({"status": "healthy"})

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(APIView):
    def get(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        try:
            logger.info(f"Category creation completed", extra={"correlation_id": correlation_id})
            categories = CategoryManager.list_all_categories()
            logger.info(f"Fetched all products successfully - total categories: {len(categories)}", extra={"correlation_id": correlation_id})
            return JsonResponse({"data": categories}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Error fetching products: {str(e)}", extra={"correlation_id": correlation_id})
            return JsonResponse(
                {"error": "Failed to retrieve categories."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        logger.info("Category creation started", extra={"correlation_id": correlation_id})
        serializer_data, error = CategoryManager.create_category(request.data)
        if error:
            logger.error(f"Error creating category: {error}", extra={"correlation_id": correlation_id})
            return JsonResponse({"errors": error}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Category creation completed", extra={"correlation_id": correlation_id})
        return JsonResponse({"data": serializer_data}, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class ProductsView(APIView):
    def get(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        try:
            logger.info(f"Product retrieval started", extra={"correlation_id": correlation_id})
            products = ProductManager.list_all_products()
            logger.info(f"Product retrieval completed - total products: {len(products)}", extra={"correlation_id": correlation_id})
            return JsonResponse({"data": products}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Error fetching products: {str(e)}", extra={"correlation_id": correlation_id})
            return JsonResponse(
                {"error": "Failed to retrieve products."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        correlation_id = request.correlation_id  # Get correlation id from middleware
        logger.info("Product creation started", extra={"correlation_id": correlation_id})
        serializer_data, error = ProductManager.create_product(request.data)
        if error:
            logger.error(f"Error creating product: {error}", extra={"correlation_id": correlation_id})
            return JsonResponse({"errors": error}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Product creation completed", extra={"correlation_id": correlation_id})
        return JsonResponse({"data": serializer_data}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_product_by_id(request, product_id):
    correlation_id = request.correlation_id  # Get correlation id from middleware
    try:
        logger.info(f"Product retrieval by ID started", extra={"correlation_id": correlation_id})
        product = ProductManager.get_product_by_id(product_id)
        logger.info(f"Product retrieval by ID completed", extra={"correlation_id": correlation_id})
        return JsonResponse(product, status=status.HTTP_200_OK)
    except Products.DoesNotExist:
        logger.error(f"Product not found: {product_id}", extra={"correlation_id": correlation_id})
        return JsonResponse({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(f"Error fetching product by ID: {str(e)}", extra={"correlation_id": correlation_id})
        return JsonResponse({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def filter_products(request):
    correlation_id = request.correlation_id  # Get correlation id from middleware
    try:
        logger.info(f"Product filtering started", extra={"correlation_id": correlation_id})
        filters = request.GET
        products = ProductManager.filter_products(filters)
        logger.info(f"Product filtering completed - total products: {len(products)}", extra={"correlation_id": correlation_id})
        return JsonResponse(products, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(f"Error filtering products: {str(e)}", extra={"correlation_id": correlation_id})
        return JsonResponse({"error": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def check_stock(request):
    correlation_id = request.correlation_id  # Get correlation id from middleware
    try:
        logger.info(f"Stock check started", extra={"correlation_id": correlation_id})
        items = request.data.get("items", [])

        if not items:
            logger.error(f"No items provided for stock check", extra={"correlation_id": correlation_id})
            return JsonResponse({"error": "No items provided"}, status=status.HTTP_400_BAD_REQUEST)

        result, error = ProductManager.check_stock(items)
        if error:
            logger.error(f"Stock check failed: {error}", extra={"correlation_id": correlation_id})
            return JsonResponse({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Stock check completed - available items: {result}", extra={"correlation_id": correlation_id})
        return JsonResponse(result, status=status.HTTP_200_OK)
    except Exception as e:
        logger.exception(f"Error checking stock: {str(e)}", extra={"correlation_id": correlation_id})
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
