from django.shortcuts import render, redirect
from .models import Post, Author, Comment
from django.views import generic
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


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


    return render(request, 'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})


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
        messages.success(request, 'Комментарий успешно отправлен.')
        return redirect(post)

    return render(request, 'blog/comment.html', {'form': form, 'comment': comment, 'post': post})


class PostCreate(CreateView, PermissionRequiredMixin):
    model = Post
    fields = ['title', 'description', 'tag']
    permission_required = 'blog.add_post'


    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpdate(UpdateView, PermissionRequiredMixin):
    model = Post
    fields = ['title', 'description', 'tag']
    permission_required = 'blog.add_post'


class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    permission_required = 'blog.add_post'
    success_url = reverse_lazy('posts')



