from django.urls import path

from . import views


urlpatterns = [
	path('', views.donation_view, name='donation'),
    path('completed/', views.donation_completed_view, name='donation_completed'),
]
