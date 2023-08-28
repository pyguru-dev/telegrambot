from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def instruction_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'instruction.html')
