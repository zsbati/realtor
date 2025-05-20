from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    """Form for registering new users."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserUpdateForm(UserChangeForm):
    """Form for updating user information."""
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff', 'is_active')

class PasswordChangeForm(forms.Form):
    """Form for changing user password."""
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

class CustomUserChangeForm(forms.Form):
    """Form for superusers to change other users' passwords."""
    new_password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    confirm_password = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem.')
        return cleaned_data

    def save(self):
        if self.user:
            self.user.set_password(self.cleaned_data['new_password'])
            self.user.save()
            return self.user
        return None
