from django.shortcuts import render
from .models import Post, Author, Comment
from django.views import generic
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    num_posts = Post.objects.all().count()
    num_authors = Author.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_posts': num_posts,
                 'num_authors': num_authors},
    )


class PostListView(generic.ListView):
    model = Post
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author


@login_required
def write_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.all
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user.username
            new_comment.save()
            messages.success(request, 'Комментарий успешно отправлен.')
            return HttpResponseRedirect(reverse('comment', args=[post.id]))
    else:
        form = CommentForm()

    return render(request, 'blog/comment.html', {'form': form, 'comments': comments, 'post': post})


class PostCreate(CreateView, PermissionRequiredMixin):
    model = Post
    fields = ['title', 'description']
    permission_required = 'blog.add_post'

    def form_valid(self, form):
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)


class PostUpdate(UpdateView, PermissionRequiredMixin):
    model = Post
    fields = '__all__'
    permission_required = 'blog.add_post'


class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Post
    fields = '__all__'
    permission_required = 'blog.add_post'
    # success_url = reverse('post')



