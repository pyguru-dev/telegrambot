from django.urls import path

from . import views


app_name = 'telegram_bot_menu'
urlpatterns = [
	path('<int:telegram_bot_id>/', views.telegram_bot_view, name='telegram_bot'),
	path('<int:telegram_bot_id>/users/', views.telegram_bot_users_view, name='telegram_bot_users'),
	path('<int:telegram_bot_id>/database/', views.telegram_bot_database_view, name='telegram_bot_database'),
	path('<int:telegram_bot_id>/plugins/', views.telegram_bot_plugins_view, name='telegram_bot_plugins'),
	path('<int:telegram_bot_id>/constructor/', views.telegram_bot_constructor_view, name='telegram_bot_constructor'),
]
