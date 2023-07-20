from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def instruction(request: HttpRequest) -> HttpResponse:
	return render(request, 'instruction.html')
