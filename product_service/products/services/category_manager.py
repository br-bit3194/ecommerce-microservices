# products/services/category_manager.py

from ..models import Category
from ..serializers import CategorySerializer
from django.db import IntegrityError
from ..utils import parse_serializer_errors

class CategoryManager:

    @staticmethod
    def list_all_categories():
        """
        Retrieve all categories.
        """
        categories = Category.objects.all()
        return CategorySerializer(categories, many=True).data

    @staticmethod
    def create_category(category_data):
        """
        Create a new category.

        Returns:
            - (serialized_data, None) if successful
            - (None, errors) if validation or integrity error
        """
        serializer = CategorySerializer(data=category_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return serializer.data, None
            except IntegrityError:
                # Handle unique constraint or DB-level errors
                return None, {"error": "Category already exists"}
        else:
            parsed_errors = parse_serializer_errors(serializer.errors)
            return None, parsed_errors