from django.contrib import admin
from .models import Post, Author, Comment

admin.site.register(Post)
admin.site.register(Comment)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('blogger',)
    prepopulated_fields = {'slug': ('blogger',)}

admin.site.register(Author, AuthorAdmin)