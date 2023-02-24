from django.urls import path
from user.views import *

urlpatterns = [
	path('auth/<int:user_id>/<str:password>/', auth),
]