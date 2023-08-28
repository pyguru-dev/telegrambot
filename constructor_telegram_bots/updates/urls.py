from django.urls import path

from . import views


urlpatterns = [
	path('', views.updates_view, name='updates'),
    path('<int:update_id>/', views.update_view, name='update'),
]
