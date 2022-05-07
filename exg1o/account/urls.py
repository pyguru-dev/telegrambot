from django.urls import path
from account.views import *

urlpatterns = [
	path('view/<str:account>/', view_profile),
	path('sign_out/', sign_out),
]