from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    # re_path(r'^posts/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post-detail'),
    re_path(r'^posts/(?P<pk>\d+)$', views.post_detail, name='post-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^authors/(?P<slug>[\w-]+)/$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^posts/(?P<pk>\d+)/comment/$', views.write_comment, name='comment'),
    path('posts/create/', views.PostCreate.as_view(), name='post-create'),
    re_path(r'^posts/(?P<pk>\d+)/update/$', views.PostUpdate.as_view(), name='post-update'),
    re_path(r'^posts/(?P<pk>\d+)/delete/$', views.PostDelete.as_view(), name='post-delete'),
    re_path(r'^posts/tag/(?P<slug>[\w-]+)$', views.PostByTagListView.as_view(), name='posts-by-tag'),
    path('search/', views.post_search, name='post-search'),
    path('register/', views.register, name='register'),
]