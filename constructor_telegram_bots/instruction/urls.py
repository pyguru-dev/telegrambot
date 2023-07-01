from django.urls import path

from instruction import views


urlpatterns = [
	path('', views.instruction, name='instruction'),
]
