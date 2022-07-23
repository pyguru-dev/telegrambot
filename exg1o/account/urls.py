from django.urls import path
from account.views import *

urlpatterns = [
	path('<str:username>/upgrade/', upgrade_account_page),
	path('view/<str:username>/', view_profile_page),
	path('sign_out/<str:username>/', sign_out),
]