from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def privacy_policy_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'privacy_policy.html')
