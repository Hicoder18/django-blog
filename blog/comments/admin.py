from django.contrib import admin

# Register your models here.
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'essay', 'created_time']
    fields = ['name', 'text', 'essay']


admin.site.register(Comment, CommentAdmin)
