from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView
# from django.contrib.auth import get_user_model
# from rest_framework.response import Response
# from django.http import Http404

from .models import Order
from .serializers import OrderSerializer

# User = get_user_model()

# class ConfirmitionView(APIView):
    
#     def get(self, request):
#         orders = Order.objects.all()
#         serializer = OrderConfSerializer(orders, many=True).data
#         if serializer.get('confirmition_code') == request.confirmition_code:
#             orders['confirmition'] = True
#             orders['confirmition_code'] = ''
#             orders.save()
#             return Response('Вы успешно подтвердили заказ')
#         else:
#             raise Http404


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)