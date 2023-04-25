from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from scripts.decorators import SiteDecorators

@SiteDecorators.get_global_context
def home(request: WSGIRequest, context: dict) -> HttpResponse:
	return render(request=request, template_name='home.html', context=context)
