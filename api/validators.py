from django.utils.dateparse import parse_datetime
from django.http import JsonResponse

def model_length_validator(model: str) -> bool:
    return len(model) == 2

def version_length_validator(version: str) -> bool:
    return len(version) == 2



def created_datetime_validator(created):
    try:
        parsed_datetime = parse_datetime(created)
    except ValueError:
        return False
    return parsed_datetime is not None


