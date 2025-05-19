from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('password/change/', views.change_password, name='change_password'),
    path('user/<int:pk>/password/', views.change_user_password, name='change_user_password'),
]
