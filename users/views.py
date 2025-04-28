from django.shortcuts import render
from django.contrib import messages
from .forms import CustomUserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.Post)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            message.success(request, f'Аккаунт для {username} успешно создан')
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})