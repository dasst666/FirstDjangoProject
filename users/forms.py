from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем help_text у всех полей
        for field_name in self.fields:
            self.fields[field_name].help_text = ''

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']