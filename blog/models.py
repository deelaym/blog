from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text='Содержание поста.')

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class Author(models.Model):
    blogger = models.CharField(max_length=20)
    bio = models.TextField(max_length=1000, help_text='Биография автора.')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'slug': self.slug})


    def __str__(self):
        return self.blogger


class Comment(models.Model):
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100, help_text='Содержание комментария.')

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return self.description

