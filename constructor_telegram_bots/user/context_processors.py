from .models import User


def users(*args, **kwargs) -> dict:
    return {'users': User.objects.all()}
