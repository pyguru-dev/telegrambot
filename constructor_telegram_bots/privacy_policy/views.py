from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from scripts.decorators import SiteDecorators

@SiteDecorators.get_user_data
def privacy_policy(request: WSGIRequest, data: dict) -> HttpResponse:
	return render(request=request, template_name='privacy_policy.html', context=data)
