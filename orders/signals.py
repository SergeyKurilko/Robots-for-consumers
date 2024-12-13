from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order
from robots.models import Robot

@receiver(pre_save, sender=Order)
def check_robot_availability(sender, instance, **kwargs):
    robot_serial = instance.robot_serial
    if not Robot.objects.filter(serial=robot_serial).exists():
        instance.status = 'pending'
    else:
        instance.status = 'in_stock'