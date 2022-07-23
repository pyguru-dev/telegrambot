from django.urls import path
from account.views import *

urlpatterns = [
	path('<str:username>/upgrade/', upgrade_account),
	path('view/<str:username>/', view_profile),
	path('sign_out/<str:username>/', sign_out),
]