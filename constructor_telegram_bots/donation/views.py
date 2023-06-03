from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def donation(request: WSGIRequest) -> HttpResponse:
	return render(request, 'donation.html')

def donation_completed(request: WSGIRequest) -> HttpResponse:
	return render(request, 'donation_completed.html')
