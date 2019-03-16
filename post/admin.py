from django.contrib import admin
from django.contrib import admin

# Register your models here.

from .models import Post
from .models import Category
from .models import Comment
from .models import CommentChild

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(CommentChild)