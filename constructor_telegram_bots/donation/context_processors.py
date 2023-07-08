from django.http import HttpRequest

from donation.models import Donation


def donations(request: HttpRequest) -> dict:
    return {'donations': Donation.objects.all()}
