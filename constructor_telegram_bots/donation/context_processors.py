from .models import Donation


def donations(*args, **kwargs) -> dict:
    return {'donations': Donation.objects.all()}
