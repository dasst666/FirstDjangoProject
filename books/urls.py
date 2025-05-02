from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name = "index")
]

urlpatterns += [
    path('<int:pk>/', views.BookDetailView.as_view(), name = 'book-detail'),
    path('', views.BookListView.as_view(), name = 'book-list'),
    # path('<int:pk>/add', views.add_book_to_user, name = 'book-add'),
    path('<int:pk>/status/', views.update_user_book_status, name='book-status'),
]