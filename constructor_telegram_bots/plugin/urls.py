from django.urls import path

from . import views


urlpatterns = [
	path('_/<int:telegram_bot_id>/', views.PluginsView.as_view(), name='plugins'),
    path('<int:plugin_id>/', views.PluginView.as_view(), name='plugin'),
	path('<int:plugin_id>/logs/', views.PluginLogsView.as_view(), name='plugin_logs'),
]
