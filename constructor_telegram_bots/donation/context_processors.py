from .models import *


def donations(*args, **kwargs) -> dict:
	return {'donations': Donation.objects.all()}

def donation_sections(*args, **kwargs) -> dict:
	return {'donation_sections': DonationSection.objects.all()}
