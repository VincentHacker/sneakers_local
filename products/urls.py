from django.urls import path
from .views import ProductViewSet, CommentViewSet, ImageView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('comments', CommentViewSet)
router.register('image', ImageView)

urlpatterns = []
urlpatterns += router.urls # urlpatterns.extend(router.urls)