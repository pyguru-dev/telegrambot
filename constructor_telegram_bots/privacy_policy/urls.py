from django.urls import path

from . import views


urlpatterns = [
	path('', views.privacy_policy_view, name='privacy_policy'),
]
