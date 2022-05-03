from django.urls import path
from authorization.views import *

urlpatterns = [
	path('authorization/', authorization),
	path('authorization/authorize_in_account/', authorize_in_account),
]
