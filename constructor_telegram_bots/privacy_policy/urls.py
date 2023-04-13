from django.urls import path

from privacy_policy import views

urlpatterns = [
	path('', views.privacy_policy),
]
