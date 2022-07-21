from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from products.filters import ProductPriceFilter

from .models import Favorites, Like, Product, CommentRating, Brand, SneakersType
from .serializers import BrandSerializer, FavoritesSerializer, LikeSerializer, ProductSerializer, ReviewSerializer, SnekersTypeSerializer
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
    
    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user

        try:
            like = Like.objects.filter(product_id=product, author=user)
            mauler = not like[0].like
            if mauler:
                like[0].save()
            else:
                like.delete()
            message = 'Нравится' if like else 'Не нравится'
        except IndexError:
            Like.objects.create(product_id=product.id, author=user, like=True)
            message = 'Нравится'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            favorites = Favorites.objects.filter(product_id=product, author=user)
            mauler = not favorites[0].favorites
            if mauler:
                favorites[0].save()
            else:
                favorites.delete()
            message = 'В избранном' if favorites else 'Не в избранном'
        except IndexError:
            Favorites.objects.create(product_id=product.id, author=user, favorites=True)
            message = 'В избранном'
        return Response(message, status=200)


class CommentViewSet(ModelViewSet):
    queryset = CommentRating.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


class BrandViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class SneakersTypeViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = SneakersType.objects.all()
    serializer_class = SnekersTypeSerializer

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class LikeViews(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FavoritesViews(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer