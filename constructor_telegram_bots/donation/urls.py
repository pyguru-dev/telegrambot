from django.urls import path

from donation import views


urlpatterns = [
	path('', views.donation, name='donation'),
]
