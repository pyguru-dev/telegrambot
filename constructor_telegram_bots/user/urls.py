from django.urls import path

from user import views


urlpatterns = [
	path('login/<int:user_id>/<str:confirm_code>/', views.user_login),
    path('logout/', views.user_logout),

    path('get-added-telegram-bots/', views.get_user_added_telegram_bots),
]
