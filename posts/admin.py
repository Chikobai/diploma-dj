from django.contrib import admin
from .models import Post, PostType, UrlType


admin.site.register(Post)
admin.site.register(PostType)
admin.site.register(UrlType)
