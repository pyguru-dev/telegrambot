from django.core.handlers.wsgi import WSGIRequest

from donation.models import Donation


def donations(request: WSGIRequest) -> dict:
    return {'donations': Donation.objects.all()}
