from django.urls import path

from . import views


urlpatterns = [
	path('plugins/', views.Plugins.as_view(), name='plugins'),
	path('plugin/logs/', views.PluginLogs.as_view(), name='plugin_logs'),
]
