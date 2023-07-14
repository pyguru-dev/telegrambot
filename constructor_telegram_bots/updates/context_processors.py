from .models import Update


def updates(*args, **kwargs) -> dict:
    return {'updates': Update.objects.all()}
