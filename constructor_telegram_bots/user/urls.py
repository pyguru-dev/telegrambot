from django.urls import path

from user import views

urlpatterns = [
	path('auth/<int:user_id>/<str:confirm_code>/', views.user_auth),
    path('get_added_telegram_bots/', views.get_user_added_telegram_bots),
]