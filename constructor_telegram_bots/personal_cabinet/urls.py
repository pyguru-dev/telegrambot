from django.urls import path

from personal_cabinet import views


urlpatterns = [
	path('', views.personal_cabinet),
	path('<int:telegram_bot_id>/', views.telegram_bot_menu),
]
