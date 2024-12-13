from django.contrib import admin
from orders.models import Order
from django.forms import ModelForm


class OrderAdminForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'robot_serial']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'robot_serial', 'status']
    form = OrderAdminForm
