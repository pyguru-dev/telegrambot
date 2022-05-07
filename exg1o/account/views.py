from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
import global_methods as GlobalMethods

# Create your views here.
def view_profile(request: WSGIRequest, account: str):
	data = GlobalMethods.get_navbar_buttons_data(request)
	return render(request, 'view_profile.html', data)