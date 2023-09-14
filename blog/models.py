from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, help_text='Содержание поста.')
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return self.title


class Author(models.Model):
    user = models.CharField(max_length=20)
    bio = models.TextField(max_length=1000, help_text='Биография автора.')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'slug': self.slug})


    def __str__(self):
        return self.user


class Comment(models.Model):
    user = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, help_text='Содержание комментария.')
    post = models.ForeignKey('Post', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.description

