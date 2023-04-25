from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from scripts.decorators import SiteDecorators

@SiteDecorators.get_global_context
def privacy_policy(request: WSGIRequest, context: dict) -> HttpResponse:
	return render(request=request, template_name='privacy_policy.html', context=context)
