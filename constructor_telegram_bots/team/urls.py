from django.urls import path

from team import views


urlpatterns = [
	path('', views.team, name='team'),
]
