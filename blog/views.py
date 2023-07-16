from django.shortcuts import render
from .models import Post, Author, Comment
from django.views import generic



def index(request):
    num_posts = Post.objects.all().count()
    num_authors = Author.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_posts':num_posts,
                 'num_authors':num_authors},
    )


class PostListView(generic.ListView):
    model = Post
    pagination = 5

class PostDetailView(generic.DetailView):
    model = Post

class AuthorListView(generic.ListView):
    model = Author
    pagination = 5

class AuthorDetailView(generic.DetailView):
    model = Author