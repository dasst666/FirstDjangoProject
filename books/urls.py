from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name = "index")
]

urlpatterns += [
    path('<int:pk>/', views.BookDetailView.as_view(), name = 'book-detail'),
    path('', views.BookListView.as_view(), name = 'book-list'),
    path('<int:pk>/status/', views.update_user_book_status, name='book-status'),
]

urlpatterns += [
    path('search/', views.search_books, name='book-search'),
    path('import/', views.import_book, name='import-book'),
]