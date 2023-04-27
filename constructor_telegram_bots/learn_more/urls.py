from django.urls import path

from learn_more import views


urlpatterns = [
	path('', views.learn_more),
]
