from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from scripts.decorators import SiteDecorators

@SiteDecorators.get_global_context
def donation(request: WSGIRequest, context: dict) -> HttpResponse:
	return render(request=request, template_name='donation.html', context=context)
