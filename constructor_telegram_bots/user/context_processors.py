from django.http import HttpRequest

from user.models import User


def users(request: HttpRequest) -> dict:
    return {'users': User.objects.all()}
