from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from scripts.decorators import SiteDecorators

@SiteDecorators.get_user_data
def donation(request: WSGIRequest, data: dict) -> HttpResponse:
	return render(request=request, template_name='donation.html', context=data)
