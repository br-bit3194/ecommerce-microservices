# products/services/product_manager.py
from django.db.models import Q
from django.db import IntegrityError

from ..models import Products
from ..serializers import ProductSerializer
from ..utils import parse_serializer_errors


class ProductManager:

    @staticmethod
    def list_all_products():
        products = Products.objects.all()
        return ProductSerializer(products, many=True).data

    @staticmethod
    def get_product_by_id(product_id):
        product = Products.objects.get(id=product_id)
        return ProductSerializer(product).data

    @staticmethod
    def filter_products(filters):
        name = filters.get('name')
        description = filters.get('description')
        price = filters.get('price')

        query = Q()
        if name:
            query &= Q(name__icontains=name)
        if description:
            query &= Q(description__icontains=description)
        if price:
            query &= Q(price=float(price))

        products = Products.objects.filter(query)
        return ProductSerializer(products, many=True).data

    @staticmethod
    def create_product(product_data):
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return serializer.data, None
            except IntegrityError:
                return None, {"error": "Product with given details already exists"}
        else:
            return None, parse_serializer_errors(serializer.errors)

    @staticmethod
    def check_stock(items):
        try:
            result = []
            for item in items:
                product_id = item["product_id"]
                requested_qty = item["quantity"]

                try:
                    product = Products.objects.get(id=product_id)
                    available = product.stock_quantity >= requested_qty

                    if not available:
                        return None, {"error": f"Product id={product_id}, name='{product.name}' is out of stock"}
                    result.append({"product_id": product_id, "available": available})
                except Products.DoesNotExist:
                    return None, {"error": f"Product with ID {product_id} does not exist"}

            return {"success": True, "items": result}, None

        except Exception as e:
            return None, {"error": str(e)}
