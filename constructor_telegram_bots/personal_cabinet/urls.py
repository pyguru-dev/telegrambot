from django.urls import path

from . import views


urlpatterns = [
	path('', views.personal_cabinet_view, name='personal_cabinet'),
]
