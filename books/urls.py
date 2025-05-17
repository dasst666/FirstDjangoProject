from django.urls import path

from . import views

urlpatterns = [
]

urlpatterns += [
    path('<int:pk>/', views.BookDetailView.as_view(), name = 'book-detail'),
    path('', views.BookListView.as_view(), name = 'book-list'),
    path('<int:pk>/status/', views.UserBookUpdateView.as_view(), name='book-status'),
]

urlpatterns += [
    path('search/', views.search_books, name='book-search'),
    path('import/', views.import_book, name='import-book'),
]

# urlpatterns += [
#     path('<int:pk>/remove/', views.remove_book_from_user, name='remove-book')
# ]

urlpatterns += [
    # ... другие маршруты
    path('remove-book/<int:pk>/', views.remove_book_from_user, name='remove-book'),
]