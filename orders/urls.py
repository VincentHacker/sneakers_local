from rest_framework.routers import DefaultRouter
# from django.urls import path

from orders.views import OrderViewSet


router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    # path('confirmition/<str:confirmition_code>/', ConfirmitionView.as_view()),
    ]

urlpatterns += router.urls