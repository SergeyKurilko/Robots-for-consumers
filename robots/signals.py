from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from robots.models import Robot
from orders.models import Order
from robots.tasks import send_notification_email


@receiver(pre_save, sender=Robot)
def generate_serial_on_create(sender, instance, **kwargs):
        instance.serial = f'{instance.model}-{instance.version}'


@receiver(post_save, sender=Robot)
def notify_customer_on_robot_availability(sender, instance, **kwargs):
        """
        Проверяет наличие заказа, ожидающего Robot с таким serial,
        вызывает задачу на отправку писем тем, кто заказывал такого
        робота
        """

        # Коллекция заказов со статусом pending и полем robot_serial
        # соответствующим instance.serial
        pending_orders = Order.objects.filter(status="pending",
                                              robot_serial=instance.serial)

        # Ставим задачу отправки письма всем ожидающим
        for order in pending_orders:
                send_notification_email(
                        customer_email=order.customer.email,
                        robot_serial=instance.serial
                )

                # Обновляем статус заказа
                order.status = "in_stock"
                order.save()
