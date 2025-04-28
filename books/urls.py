from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name = "index")
]

urlpatterns += [
    path('<int:pk>/', views.BookDetailView.as_view(), name = 'book-detail'),
    path('', views.BookListView.as_view(), name = 'book-list')
]