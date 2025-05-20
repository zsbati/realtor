from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserUpdateForm, PasswordChangeForm, CustomUserChangeForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    """List all users."""
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def change_user_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, user=user)
        if form.is_valid():
            try:
                # Save the form which will handle setting the password
                form.save()
                messages.success(request, 'Senha alterada com sucesso.')
                return redirect('users:user_list')
            except Exception as e:
                messages.error(request, f'Erro ao alterar senha: {str(e)}')
        else:
            messages.error(request, 'Formulário inválido. Por favor, corrija os erros.')
    else:
        form = CustomUserChangeForm(user=user)
    return render(request, 'users/change_password.html', {'form': form, 'user': user})

@login_required
def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} has been created.')
            return redirect('users:user_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_user(request, user_id):
    """Update user information."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuário {user.username} foi atualizado.')
            return redirect('users:user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/update_user.html', {'form': form, 'user': user})



@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    """Delete a user."""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'Usuário {user.username} foi eliminado.')
        return redirect('users:user_list')
    return render(request, 'users/delete_user.html', {'user': user})
