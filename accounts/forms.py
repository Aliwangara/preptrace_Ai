from django import forms
from .models import User,Profile

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email","password"]

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'tech_stack', 'cv']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({
            'placeholder': 'Your career role (e.g., Backend Developer, UX Designer)',
            'id': 'role-input',          # <-- Add this
            'autocomplete': 'off'
        })
        self.fields['tech_stack'].widget.attrs.update({
            'placeholder': 'Technologies you use (optional)'
        })