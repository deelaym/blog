from django.contrib import admin
from .models import Post, Author, Comment

admin.site.register(Post)
admin.site.register(Comment)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user',)
    prepopulated_fields = {'slug': ('user',)}

admin.site.register(Author, AuthorAdmin)