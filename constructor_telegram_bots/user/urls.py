from django.urls import path

from user import views


urlpatterns = [
	path('login/<int:user_id>/<str:confirm_code>/', views.user_login),
    path('logout/', views.user_logout),

    path('get-telegram-bots/', views.get_user_telegram_bots),
]
