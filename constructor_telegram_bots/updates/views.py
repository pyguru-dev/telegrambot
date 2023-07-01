from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render
from django.utils.translation import gettext as _

from updates.decorators import check_update_id

from updates.models import Update


def updates(request: WSGIRequest) -> HttpResponse:
	return render(request, 'updates.html')

@check_update_id
def update(request: WSGIRequest, update: Update) -> HttpResponse:
	return render(request, 'update.html', {'update': update})
