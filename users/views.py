from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserRegisterForm

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} успешно создан')
            return redirect('login')
    else:
        form = CustomUserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def profile_view(request):
    user = request.user
    books = user.books.all()

    return render(request, 'users/profile.html', {'user': user, 'books': books})