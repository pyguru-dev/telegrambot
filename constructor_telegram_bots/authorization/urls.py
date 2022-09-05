from django.urls import path
from authorization.views import *

urlpatterns = [
	path('authorization/', authorization_page),
	path('authorization/authorize_in_account/', authorize_in_account),
]
