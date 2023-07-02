from django.core.handlers.wsgi import WSGIRequest

from updates.models import Update


def updates(request: WSGIRequest) -> dict:
    return {'updates': Update.objects.all()}
