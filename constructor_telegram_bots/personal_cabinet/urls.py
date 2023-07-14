from django.urls import path

from . import views


urlpatterns = [
	path('', views.personal_cabinet, name='personal_cabinet'),
	path('<int:telegram_bot_id>/', views.telegram_bot_menu, name='telegram_bot_menu'),
]
