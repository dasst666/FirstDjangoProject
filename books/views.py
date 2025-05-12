from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Book, UserBook, Author
from .forms import UserBookForm

# Create your views here.

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

from django.contrib.auth.decorators import login_required


from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
class UserBookUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBook
    form_class = UserBookForm
    template_name = 'books/book_status_form.html'

    def get_object(self):
        book = get_object_or_404(Book, pk.self.kwargs['pk'])

        user_book, _ = UserBook.objects.get_or_create(user=self.request.user, book=book)
        return user_book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.kwargs['pk']})

import requests

def search_books(request):
    query = request.GET.get('q')
    results = []
    local_results = []

    if query:
        local_results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )

        if not local_results.exists():
            response = requests.get('https://www.googleapis.com/books/v1/volumes', params={'q': query, 'langRestrict': 'ru'})
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    volume_info = item['volumeInfo']
                    results.append({
                        'title': volume_info.get('title'),
                        'author': ', '.join(volume_info.get('authors', [])),
                        'description': volume_info.get('description', ''),
                        'image': volume_info.get('imageLinks', {}).get('thumbnail', '')
                    })

    return render(request, 'books/search_result.html', {'results': results, 'local_results': local_results})

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
@login_required
def import_book(request):
    title = request.POST.get('title')
    author = request.POST.get('author')
    summary = request.POST.get('summary')
    image = request.POST.get('image')

    try:
        first_name, last_name = author.split(' ', 1)
    except:
        first_name = author
        last_name = ' '
    
    # Получаем или создаём автора
    author_obj, _ = Author.objects.get_or_create(first_name=first_name, last_name=last_name)

    # Получаем или создаём книгу
    book, _ = Book.objects.get_or_create(title=title, summary=summary, author=author_obj, defaults={'image_url': image})

    # Добавляем книгу пользователю
    UserBook.objects.get_or_create(user=request.user, book=book, defaults={'status': 'want'})

    return JsonResponse({'status': 'success', 'message': 'Книга добавлена'})

