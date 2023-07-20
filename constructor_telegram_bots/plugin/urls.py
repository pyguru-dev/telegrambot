from django.urls import path

from . import views


urlpatterns = [
	path('_/<int:telegram_bot_id>/', views.PluginsView.as_view(), name='plugins'),
    path('<int:plugin_id>/', views.PluginView.as_view(), name='plugin'),
    path('_/<int:telegram_bot_id>/logs/', views.get_plugins_logs_view, name='plugins_logs'),
	path('<int:plugin_id>/logs/', views.add_plugin_log_view, name='plugin_logs'),
]
