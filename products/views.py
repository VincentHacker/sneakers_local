from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import permissions

from products.filters import ProductPriceFilter

from .models import Product, CommentRating, Image
from .serializers import ProductSerializer, ReviewSerializer, ImageSerializer
from .permissions import IsAuthor


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_class = ProductPriceFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class CommentViewSet(ModelViewSet):
    queryset = CommentRating.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer