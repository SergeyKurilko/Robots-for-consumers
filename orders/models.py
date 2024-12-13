from django.db import models

from customers.models import Customer


class Order(models.Model):
    STATUS_CHOICES = [
        ('1', 'pending'),
        ('2', 'completed'),
    ]

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5,blank=False, null=False)
    status = models.CharField(max_length=20, default='1', choices=STATUS_CHOICES)
