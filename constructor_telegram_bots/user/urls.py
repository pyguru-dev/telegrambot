from django.urls import path

from user import views


urlpatterns = [
	path('login/<int:id>/<str:confirm_code>/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
	path('get-telegram-bots/', views.get_telegram_bots, name='get_telegram_bots'),
]
