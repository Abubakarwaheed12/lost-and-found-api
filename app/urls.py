from django.urls import path, include
from .views import UserProductsListView, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('products/user/<int:user_id>/', UserProductsListView.as_view(), name='user-products-list'),
    path('', include(router.urls)),
]
