from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'agenda'

urlpatterns = [
    # Dashboard URL
    path('', views.dashboard, name='dashboard'),
    # Visit URLs
    path('visits/', views.visit_list, name='visit_list'),
    path('visit/<int:pk>/', views.visit_detail, name='visit_detail'),
    path('visit/new/', views.visit_create, name='visit_create'),
    path('visit/<int:pk>/edit/', views.visit_edit, name='visit_edit'),
    path('visit/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    # User management URLs
    path('password/change/', views.password_change, name='password_change'),
    # Reports URL
    path('reports/', views.reports, name='reports'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='agenda/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),

    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
