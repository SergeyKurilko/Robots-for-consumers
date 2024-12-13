from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(customer_email, robot_serial):
    subject = 'Робот в наличии'
    message = f"""
    Добрый день!
    Недавно вы интересовались нашим роботом модели {robot_serial[:2]}, версии {robot_serial[-2:]}. 
    Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами
    """
    from_email = 'noreply@example.com'
    recipient_list = [customer_email]

    send_mail(subject, message, from_email, recipient_list)