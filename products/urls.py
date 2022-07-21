from django.urls import path
from .views import FavoritesViews, LikeViews, ProductViewSet, CommentViewSet, BrandViewSet, SneakersTypeViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('comments', CommentViewSet)
router.register('brand', BrandViewSet)
router.register('snekers_type', SneakersTypeViewSet)
router.register('like', LikeViews)
router.register('favorites', FavoritesViews)

urlpatterns = []
urlpatterns += router.urls # urlpatterns.extend(router.urls)