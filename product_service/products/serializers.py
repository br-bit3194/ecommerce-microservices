from rest_framework import serializers
from .models import Products, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"