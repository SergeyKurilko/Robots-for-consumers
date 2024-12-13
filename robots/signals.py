from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from robots.models import Robot
from orders.models import Order


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
        pending_orders = Order.objects.filter(status="pending",
                                              robot_serial=instance.serial)
        print(pending_orders)
        pass