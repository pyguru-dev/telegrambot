from django.urls import path

from donation import views


urlpatterns = [
	path('', views.donation, name='donation'),
    path('completed/', views.donation_completed, name='donation_completed'),
]
