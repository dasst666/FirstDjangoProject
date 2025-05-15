from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length = 50, unique = True)

class Book(models.Model):
    title = models.CharField(max_length = 100)
    summary = models.TextField(max_length = 1000, help_text = 'Краткое описание книги', blank = True)

    author = models.ForeignKey('Author', on_delete = models.SET_NULL, null = True)

    owners = models.ManyToManyField(User, related_name='books', blank=True)

    image_url = models.URLField(blank=True, null = True)

    genres = models.ManyToManyField(Genre, related_name = 'books')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args = [str(self.id)])
    
    class Meta:
        ordering = ['title']

class Author(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserBook(models.Model):
    STATUS_CHOICES = [
        ('want', 'Буду читать'),
        ('reading', 'Читаю'),
        ('read', 'Прочитано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    status = models.CharField(max_length = 10, choices = STATUS_CHOICES)

    class Meta:
        unique_together = ('user', 'book')
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'


