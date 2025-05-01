from django import forms
from .models import UserBook

class UserBookForm(forms.ModelForm):
    class Meta:
        model = UserBook
        fields = ['status']