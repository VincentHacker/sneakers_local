from django.db import models
from django.contrib.auth import get_user_model
# from django.utils.crypto import get_random_string
# from django.core.mail import send_mail
# from django.conf import settings

from products.models import Product


User = get_user_model()

STATUS_CHOICE = (
    ('open', 'Открытый'),
    ('in_process', 'В обработке'),
    ('canceled', 'Отмененный'),
    ('finished', 'Завершенный')
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='orders')
    create_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=150, blank=True)
    productcs = models.ManyToManyField(Product, through='OrderItems')
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='open')
    # confirmition_code = models.CharField(max_length=20, blank=True)
    # confirmition = models.BooleanField(default=False)

    # def __str__(self) -> str:
    #     return f'Order #{self.id}'

    # def create_confirmition_code(self):
    #     code = get_random_string(20)
    #     self.confirmition_code = code
    #     self.save()
    #     return code

    # def send_confirmition_code(self):
    #     confirmition_link = f'http://127.0.0.1:8000/orders/confirmition/{self.confirmition_code}'
    #     print(self.confirmition_code)
    #     print(confirmition_link)
    #     send_mail(
    #         f'Order confirmition {self.id}', 
    #         message=confirmition_link, 
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[get_user_model().objects.get(email=self.user)], 
    #         fail_silently=False
    #     )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveSmallIntegerField(default=0)