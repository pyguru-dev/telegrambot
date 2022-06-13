from django.urls import path
from account.views import *

urlpatterns = [
	path('<str:nickname>/upgrade/', upgrade_account),
	path('view/<str:nickname>/', view_profile),
	path('sign_out/<str:nickname>/', sign_out),
]