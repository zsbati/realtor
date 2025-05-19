from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agenda'

urlpatterns = [
    # Visit URLs
    path('', views.visit_list, name='visit_list'),
    path('visit/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visit/new/', views.visit_create, name='visit_create'),
    path('visit/<int:pk>/edit/', views.visit_edit, name='visit_edit'),
    path('visit/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    # User management URLs
    path('password/change/', views.password_change, name='password_change'),

    # User management URLs
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('users/', views.user_list, name='user_list'),
    path('users/new/', views.user_add, name='user_add'),
    path('users/<int:pk>/password/', views.user_change_password, name='user_change_password'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
