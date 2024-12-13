from django.db.models.signals import pre_save
from django.dispatch import receiver
from robots.models import Robot


@receiver(pre_save, sender=Robot)
def generate_serial_on_create(sender, instance, **kwargs):
        instance.serial = f'{instance.model}-{instance.version}'