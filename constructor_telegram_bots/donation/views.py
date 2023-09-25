from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def donation_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation.html')

def donation_completed_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation_completed.html')
