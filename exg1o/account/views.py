from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth import logout
import global_methods as GlobalMethods

# Create your views here.
def view_profile(request: WSGIRequest, account: str):
	if request.user.is_authenticated:
		data = GlobalMethods.get_navbar_buttons_data(request)
		return render(request, 'view_profile.html', data)
	else:
		raise Http404('Авторизуйтесь в акканут!')

def sign_out(request: WSGIRequest):
	if request.user.is_authenticated:
		logout(request)
		return redirect('/')
	else:
		raise Http404('Авторизуйтесь в акканут!')