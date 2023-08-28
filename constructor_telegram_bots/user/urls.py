from django.urls import path

from . import views


app_name = 'user'
urlpatterns = [
	path('login/<int:user_id>/<str:confirm_code>/', views.user_login_view, name='login'),
	path('logout/', views.user_logout_view, name='logout'),
]
