from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from updates.models import Updates


def updates(request: WSGIRequest) -> HttpResponse:
	return render(request, 'updates.html', {'updates': Updates.objects.all()})
