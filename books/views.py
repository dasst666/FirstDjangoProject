from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Book

# Create your views here.

from django.shortcuts import render

def index(request):
    books = Book.objects.all()
    return render(request, 'books/index.html', {'books': books})


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()