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
