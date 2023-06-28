from django.urls import path

from updates import views


urlpatterns = [
	path('', views.updates, name='updates'),
]
