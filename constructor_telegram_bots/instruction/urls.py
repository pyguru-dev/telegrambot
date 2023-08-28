from django.urls import path

from . import views


urlpatterns = [
	path('', views.instruction_view, name='instruction'),
]
