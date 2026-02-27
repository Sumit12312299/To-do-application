from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:pk>/', views.delete_task, name='delete'),
    path('complete/<int:pk>/', views.complete_task, name='complete'),
    path('edit/<int:pk>/', views.edit_task, name='edit'),
]
