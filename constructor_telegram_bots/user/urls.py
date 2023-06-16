from django.urls import path

from user import views


urlpatterns = [
	path('login/<int:id>/<str:confirm_code>/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    
	path('get-telegram-bots/', views.get_user_telegram_bots, name='get_user_telegram_bots'),
    path('get-messages', views.get_user_messages, name='get_user_messages')
]
