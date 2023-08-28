from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .decorators import check_update_id

from .models import Update


def updates_view(request: HttpRequest) -> HttpResponse:
	return render(request, 'updates.html')

@check_update_id
def update_view(request: HttpRequest, update: Update) -> HttpResponse:
	return render(request, 'update.html', {'update': update})
