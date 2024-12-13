from django.urls import path
from api.views import CreateRobotView

app_name = 'api'

urlpatterns = [
    path('robots/', CreateRobotView.as_view())
]