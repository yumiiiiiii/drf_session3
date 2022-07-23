from django.contrib import admin
from .models import Post,Calendar, User
# Register your models here.

admin.site.register(Post)
admin.site.register(Calendar)
admin.site.register(User)