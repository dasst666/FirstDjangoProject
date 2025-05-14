from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserRegisterForm
from books.models import UserBook
from django.contrib.auth import login

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт для {user.username} успешно создан и вы вошли в систему')
            return redirect('profile')
    else:
        form = CustomUserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


def profile_view(request):
    user = request.user
    user_books = UserBook.objects.filter(user = user)

    books_want = user_books.filter(status = 'want')
    books_read = user_books.filter(status = 'read')
    books_reading = user_books.filter(status = 'reading')

    return render(
            request, 'users/profile.html', 
            {'user': user, 
            'user_books': user_books, 
            'books_read': books_read,
            'books_reading': books_reading,
            'books_want': books_want,
        })

from django.contrib.auth.models import User

def user_list_view(request):
    users = User.objects.exclude(id = request.user.id)
    return render(request, 'users/user_list.html', {'users': users})

from django.shortcuts import get_object_or_404

def public_profile_view(request, username):
    user_profile = get_object_or_404(User, username = username)
    user_books = UserBook.objects.filter(user = user_profile)

    books_want = user_books.filter(status = 'want')
    books_read = user_books.filter(status = 'read')
    books_reading = user_books.filter(status = 'reading')

    return render(request, 'users/public_profile.html', {
        'user_profile': user_profile,
        'user_books': user_books,
        'books_read': books_read,
        'books_reading': books_reading,
        'books_want': books_want,
    })
