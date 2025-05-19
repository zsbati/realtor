from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordResetView
from .models import Visit
from .forms import VisitForm, CustomUserCreationForm, CustomUserChangeForm, PasswordChangeForm
import datetime

# Create your views here.

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
                return redirect('agenda:user_list')
            return redirect('agenda:visit_list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})

@login_required
def visit_create(request):
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuário criado com sucesso.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_change_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'user_form.html', {'form': form, 'user': user})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso.')
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('agenda:visit_list')
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
