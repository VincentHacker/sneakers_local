from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from products.filters import ProductPriceFilter

from .models import Favorites, Like, Product, CommentRating, Image, Brand, SneakersType
from .serializers import BrandSerializer, FavoritesSerializer, LikeSerializer, ProductSerializer, ReviewSerializer, ImageSerializer, SnekersTypeSerializer
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
    
    @action(['POST', 'DELETE'], detail=True)
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(title=product, user=user)
            like.like = not like.like
            if like.like:
                like.save()
            else:
                like.delete()
            message = 'Нравится' if like.like else 'Не нравится'
        except Like.DoesNotExist:
            Like.objects.create(title=product, user=user, is_liked=True)
            message = 'Нравится'
        return Response(message, status=200)

    @action(['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        try:
            favorites = Favorites.objects.get(title=product, user=user)
            favorites.favorites = not favorites.favorites
            if favorites.favorites:
                favorites.save()
            else:
                favorites.delete()
            message = 'В избранном' if favorites.favorites else 'Не в избранном'
        except Favorites.DoesNotExist:
            Favorites.objects.create(title=product, user=user, is_favorite=True)
            message = 'В избранном'
        return Response(message, status=200)


class CommentViewSet(ModelViewSet):
    queryset = CommentRating.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


class FavoritesViewSet(ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthor]
        return super().get_permissions()


class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class SneakersTypeViewSet(ModelViewSet):
    queryset = SneakersType.objects.all()
    serializer_class = SnekersTypeSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['destroy', 'update', 'partial_update', 'create']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()