# from celery import shared_task
# from django.conf import settings
# from django.core.mail import send_mail

# @shared_task
# def send_activation_code(email, activation_code):
#     activation_link = f'https://dry-sands-45075.herokuapp.com/account/activation/{activation_code}'
#     send_mail(
#         'Account activation', 
#         message=activation_link, 
#         from_email=settings.EMAIL_HOST_USER, 
#         recipient_list=[email], 
#         fail_silently=False
#     )