from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def donation(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation.html')

def donation_completed(request: HttpRequest) -> HttpResponse:
	return render(request, 'donation_completed.html')
