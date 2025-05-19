from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('register/', views.register, name='register'),
    path('user/<int:user_id>/update/', views.update_user, name='update_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url='/?success=1'
    ), name='change_password'),
    path('user/<int:user_id>/password/', views.change_user_password, name='change_user_password'),
    path('logout/', auth_views.LogoutView.as_view(next_page='agenda:login'), name='logout'),
]
