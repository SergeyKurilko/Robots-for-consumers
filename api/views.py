import json
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
from openpyxl import Workbook
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


class GetWeeklyProductReportView(View):
    http_method_names = ['get']

    def get(self, request):
        last_week = datetime.now() - timedelta(days=7)

        robots = Robot.objects.filter(created__gt=last_week)
        models = robots.values_list('model', flat=True).distinct()

        # Создать excel-файл
        wb = Workbook()

        # Удалить лишний лист по умолчанию
        wb.remove(wb.active)

        for model in models:
            # Создать лист для каждой модели
            ws = wb.create_sheet(title=model)

            # Заголовки таблицы
            ws.append(['Модель', 'Версия', 'Количество за неделю'])

            # Получить данные для текущей модели
            model_robots = robots.filter(model=model)
            versions = model_robots.values_list('version', flat=True).distinct()

            for version in versions:
                count = model_robots.filter(version=version).count()
                ws.append([model, version, count])

        period_start = last_week.strftime("%d.%m.%Y")
        period_end = (datetime.now()).strftime("%d.%m.%Y")

        response = HttpResponse(
            content_type=
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = \
            (f'attachment; '
             f'filename=robot_report_{period_start}-{period_end}.xlsx')

        # Сохранить книгу в ответ
        wb.save(response)
        return response


