from django.urls import path
from django.contrib.auth import views as auth_views
from agenda.main_views import (
    dashboard, reports, visit_list, visit_detail, visit_create, 
    visit_edit, visit_delete, export_visits_to_excel, calendar_view,
    visit_calendar_events
)
from agenda.views.contract_views import contract_list, contract_detail, contract_create, contract_edit, contract_delete, export_contracts_to_excel
from django.template.loader import get_template
from django.http import HttpResponse

def check_template(request, template_name):
    try:
        template = get_template(template_name)
        return HttpResponse(f"Template found at: {template.origin}")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=404)

app_name = 'agenda'

urlpatterns = [
    # Dashboard URL
    path('', dashboard, name='dashboard'),
    # Visit URLs
    path('visits/', visit_list, name='visit_list'),
    path('visit/<int:pk>/', visit_detail, name='visit_detail'),
    path('visit/new/', visit_create, name='visit_create'),
    path('visit/<int:pk>/edit/', visit_edit, name='visit_edit'),
    path('visit/<int:pk>/delete/', visit_delete, name='visit_delete'),
    # Calendar URL
    path('calendar/', calendar_view, name='calendar_view'),
    # API endpoint for visit calendar events
    path('api/visits/calendar/', visit_calendar_events, name='visit_calendar_events'),
    # Reports URL
    path('reports/', reports, name='reports'),
    # Contract URLs
    path('contracts/', contract_list, name='contract_list'),
    path('contract/<int:pk>/', contract_detail, name='contract_detail'),
    path('contract/new/', contract_create, name='contract_create'),
    path('contract/<int:pk>/edit/', contract_edit, name='contract_edit'),
    path('contract/<int:pk>/delete/', contract_delete, name='contract_delete'),
    # Debug URL for checking templates
    path('check-template/<path:template_name>/', check_template, name='check_template'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='agenda/login.html',
        redirect_field_name='next',
        success_url='/visits/'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='agenda/logout.html',
        next_page='agenda:login'
    ), name='logout'),
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='agenda/password_reset_form.html',
        email_template_name='agenda/registration/password_reset_email.html',
        subject_template_name='agenda/registration/password_reset_subject.txt',
        success_url='/login/'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='agenda/registration/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='agenda/registration/password_reset_confirm.html',
        success_url='/login/'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='agenda/registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
