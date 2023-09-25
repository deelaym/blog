from django.shortcuts import render, redirect
from .models import Post, Author, Comment
from django.views import generic
from .forms import CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.forms import UserCreationForm


def index(request):
    num_posts = Post.objects.all().count()
    num_authors = Author.objects.all().count()
    end_post = Post.objects.latest('created')
    tags = Tag.objects.annotate(num_posts=Count('post')).order_by('-num_posts')[:10]

    return render(
        request,
        'index.html',
        context={'num_posts': num_posts,
                 'num_authors': num_authors,
                 'end_post': end_post,
                 'tags': tags},
    )


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


class PostByTagListView(generic.ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs.get('slug'))
        queryset = Post.objects.all().filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context



# class PostDetailView(generic.DetailView):
#     model = Post

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all()
    form = CommentForm()

    similar_posts = post.tags.similar_objects()[:3]


    return render(request, 'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author


@require_POST
@login_required
def write_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user.username
        comment.save()
        messages.success(request, 'Comment sent successfully.')
        return redirect(post)

    return render(request, 'blog/comment.html', {'form': form, 'comment': comment, 'post': post})


class PostCreate(CreateView, PermissionRequiredMixin):
    model = Post
    fields = ['title', 'description', 'tags']
    permission_required = 'blog.add_post'


    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpdate(UpdateView, PermissionRequiredMixin):
    model = Post
    fields = ['title', 'description', 'tags']
    permission_required = 'blog.add_post'


class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    permission_required = 'blog.add_post'
    success_url = reverse_lazy('posts')



def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'description')).filter(search=query)

    return render(request,
                   'blog/post_search.html',
                   {'form': form,
                    'query': query,
                    'results': results})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            return render(request, 'registration/register_done.html',
                           {'new_user': new_user})
            # return redirect('registration/register_done.html')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html',
                  {'form': form})