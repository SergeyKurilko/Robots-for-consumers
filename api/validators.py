from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

def model_length_validator(model: str) -> JsonResponse:
    if len(model) != 2:
        return JsonResponse({
            'error': 'Model field length must be 2 characters.',
        }, status=400)

def version_length_validator(version: str) -> JsonResponse:
    if len(version) != 2:
        return JsonResponse({
            'error': 'Version field length must be 2 characters.',
        }, status=400)

def created_datetime_validator(created):
    parsed_datetime = parse_datetime(created)
    return parsed_datetime is not None


