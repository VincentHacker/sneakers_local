from django.urls import path
from .views import ProductViewSet, CommentViewSet, ImageView, BrandViewSet, SneakersTypeViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('comments', CommentViewSet)
router.register('image', ImageView)
router.register('brand', BrandViewSet)
router.register('snekers_type', SneakersTypeViewSet)

urlpatterns = []
urlpatterns += router.urls # urlpatterns.extend(router.urls)