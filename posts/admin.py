from django.contrib import admin
from .models import Category,Author,Post,Comment,Reply
# Register your models here.

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Comment)
