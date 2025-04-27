"""
URL configuration for product_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#import views
from . import views
from django.urls import path

urlpatterns = [
    path("health/", views.health_check, name="health_check"),

    path("", views.ProductsView.as_view(), name="products"),
    path("categories/", views.CategoryView.as_view(), name="categories"),

    path("<int:product_id>/", views.get_product_by_id, name="product_detail"),
    path("filter_products/", views.filter_products, name="filter_products"),
]
