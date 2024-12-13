from django.urls import path
from api.views import CreateRobotView, GetWeeklyProductReportView

app_name = 'api'

urlpatterns = [
    path('robots/', CreateRobotView.as_view()),
    path('get-weekly-report/', GetWeeklyProductReportView.as_view())
]