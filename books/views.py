from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Book, UserBook
from .forms import UserBookForm

# Create your views here.

from django.shortcuts import render

def index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        user_book = None
        form = None 

        if self.request.user.is_authenticated:
            user_book = UserBook.objects.filter(user = self.request.user, book = book).first()
            if user_book:
                form = UserBookForm(instance = user_book)
            else:
                form = UserBookForm()
        
        context['user_book'] = user_book
        context['form'] = form

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        book = self.object

        user_book, _ = UserBook.objects.get_or_create(user=request.user, book=book)
        form = UserBookForm(request.POST, instance=user_book)
        if form.is_valid():
            form.save()
        return redirect('book-detail', pk=book.pk)
        

from django.db.models import Q

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(
                Q(title__icontains = query) | Q(author__first_name__icontains = query)
            )
        return Book.objects.all()

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def update_user_book_status(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_book, created = UserBook.objects.get_or_create(user = request.user, book = book)

    if request.method =='POST':
        form = UserBookForm(request.POST, instance = user_book)
        if form.is_valid():
            form.save()
            return redirect('book-detail', pk = pk)
    else:
        form = UserBookForm(instance = user_book)
    
    return render(request, 'books/book_status_form.html', {'form': form, 'book': book})

import requests
from django.shortcuts import render

def search_books(request):
    query = request.GET.get('q')
    results = []

    if query:
        response = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': query, 'langRestrict': 'ru'})
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                volume_info = item['volumeInfo']
                results.append({
                    'title': volume_info.get('title'),
                    'author': ', '.join(volume_info.get('authors', [])),
                    'description': volume_info.get('description', ''),
                })

    return render(request, 'books/search_result.html', {'results': results})

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Book, UserBook

@require_POST
@login_required
def import_book(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    summary = request.POST.get('summary')

    book, created = Book.objects.get_or_create(title=title, author=author, summary=summary)
    UserBook.objects.get_or_create(user=request.user, book=book, defaults={'status': 'want'})

    return redirect('profile')

