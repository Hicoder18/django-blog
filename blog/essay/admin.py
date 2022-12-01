from django.contrib import admin

from .models import Category, Tag, Essay


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ('title', 'cate', 'user', 'created_time')


admin.site.register(Category)
admin.site.register(Tag)

admin.site.site_header = '程序员博客'
admin.site.site_title = '程序员博客'
admin.site.index_title = '程序员博客管理'
