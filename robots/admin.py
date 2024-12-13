from django.contrib import admin
from django.forms import ModelForm
from robots.models import Robot

class RobotAdminForm(ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    form = RobotAdminForm
    list_display = ['serial', 'created']
    list_filter = ['serial', 'model', 'version', 'created']
