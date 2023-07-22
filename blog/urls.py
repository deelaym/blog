from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^posts/$', views.PostListView.as_view(), name='posts'),
    url(r'^posts/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post-detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^authors/(?P<slug>[\w-]+)/$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^posts/(?P<pk>\d+)/comment/$', views.write_comment, name='comment'),
    url(r'^post/create/$', views.PostCreate.as_view(), name='post-create'),
    url(r'^post/(?P<pk>\d+)/update/$', views.PostUpdate.as_view(), name='post-update'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.PostDelete.as_view(), name='post-delete'),
]