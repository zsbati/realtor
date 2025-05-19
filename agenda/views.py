from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetView
from .models import Visit
from .forms import VisitForm, CustomUserCreationForm, CustomUserChangeForm, PasswordChangeForm
import datetime

# Create your views here.

@login_required
def dashboard(request):
    today = datetime.date.today()
    
    # Get today's visits
    today_visits = Visit.objects.filter(
        scheduled_date__date=today
    ).order_by('scheduled_date')
    
    # Get upcoming visits (next 7 days)
    upcoming_visits = Visit.objects.filter(
        scheduled_date__date__gte=today,
        scheduled_date__date__lte=today + datetime.timedelta(days=7)
    ).exclude(
        scheduled_date__date=today
    ).order_by('scheduled_date')[:5]
    
    # Get recent visits (last 7 days)
    recent_visits = Visit.objects.filter(
        scheduled_date__date__gte=today - datetime.timedelta(days=7),
        scheduled_date__date__lt=today
    ).order_by('-scheduled_date')[:5]
    
    # Get visit statistics
    total_visits = Visit.objects.count()
    today_visits_count = today_visits.count()
    upcoming_visits_count = upcoming_visits.count()
    
    # Get users (only for superusers)
    users = User.objects.all() if request.user.is_superuser else None
    
    context = {
        'today_visits': today_visits,
        'upcoming_visits': upcoming_visits,
        'recent_visits': recent_visits,
        'total_visits': total_visits,
        'today_visits_count': today_visits_count,
        'upcoming_visits_count': upcoming_visits_count,
        'users': users,
        'user_list_url': 'users:user_list',
    }
    return render(request, 'dashboard.html', context)

@login_required
def reports(request):
    """View to display past visits with filtering capabilities."""
    today = datetime.date.today()
    
    # Get filter parameters from GET request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')
    visit_type = request.GET.get('visit_type')
    
    # Build filter queryset
    visits = Visit.objects.filter(
        scheduled_date__date__lt=today
    ).order_by('-scheduled_date')
    
    if start_date:
        visits = visits.filter(scheduled_date__date__gte=start_date)
    if end_date:
        visits = visits.filter(scheduled_date__date__lte=end_date)
    if status:
        visits = visits.filter(status=status)
    if visit_type:
        visits = visits.filter(visit_type=visit_type)
    
    context = {
        'visits': visits,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'visit_type': visit_type,
    }
    return render(request, 'agenda/reports.html', context)

@login_required
def visit_list(request):
    today = datetime.date.today()
    visits = Visit.objects.filter(scheduled_date__date=today).order_by('scheduled_date')
    return render(request, 'visit_list.html', {'visits': visits})

@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    return render(request, 'visit_detail.html', {'visit': visit})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Senha alterada com sucesso.')
            if request.user.is_superuser:
                return redirect('users:user_list')
            return redirect('agenda:visit_list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})

@login_required
def logout(request):
    """Custom logout view that handles GET requests."""
    auth_logout(request)
    return redirect('agenda:login')

@login_required
def visit_create(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.created_by = request.user
            visit.save()
            return redirect('agenda:visit_list')
    else:
        form = VisitForm()
    return render(request, 'visit_form.html', {'form': form})

@login_required
def visit_edit(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            visit = form.save()
            return redirect('agenda:visit_list')
    else:
        form = VisitForm(instance=visit)
    return render(request, 'visit_form.html', {'form': form})

@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == 'POST':
        visit.delete()
        return redirect('agenda:visit_list')
    return render(request, 'visit_confirm_delete.html', {'visit': visit})

# User management views

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('agenda:dashboard')
        else:
            messages.error(request, 'Nome de usuário ou senha inválidos.')
    return render(request, 'agenda/login.html')

def user_logout(request):
    logout(request)
    return redirect('agenda:login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/login/'
