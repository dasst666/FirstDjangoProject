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
        



class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.all()

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# @login_required
# def add_book_to_user(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     user = request.user
#     book.owners.add(user)
#     return redirect('book-detail', pk=pk)  # или куда хочешь

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