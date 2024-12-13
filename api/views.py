import json
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from robots.models import Robot
from api import validators


@method_decorator(csrf_exempt, name='dispatch')
class CreateRobotView(View):
    http_method_names = ['post']

    def post(self, request):
        # Проверка тела запроса на корректность
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON'
            },
                status=400)

        model = json_data.get("model")
        version = json_data.get("version")
        created =json_data.get("created")

        if not model or not version or not created:
            return JsonResponse({
                'error': 'Missing required fields'
            },
                                status=400)

        # Валидация данных
        if not validators.model_length_validator(model):
            return JsonResponse({
                'error': 'Model field length must be 2 characters.',
            }, status=400)

        if not validators.version_length_validator(version):
            return JsonResponse({
                'error': 'Version field length must be 2 characters.',
            }, status=400)

        if not validators.created_datetime_validator(created):
            return JsonResponse({
                'error': 'Invalid datetime format.'
            }, status=400)

        robot = Robot.objects.create(
            model=model,
            version=version,
            created=created
        )

        return JsonResponse(
            status=201,
            data={
                "serial": robot.serial,
                "model": robot.model,
                "version": robot.version,
                "created": robot.created,
            }
        )
