from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filterset_fields = ['type', 'category', 'date_added', 'location']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Product.objects.filter(user=self.request.user)
        return queryset




class UserProductsListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated] 
    filter_backends = [DjangoFilterBackend]
    authentication_classes = [JWTAuthentication]
    filterset_fields = ['type', 'category', 'date_added', 'location']


    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        queryset = Product.objects.filter(user=user)

        product_type = self.request.query_params.get('type', None)
        if product_type:
            queryset = queryset.filter(type=product_type)

        return queryset