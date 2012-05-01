from django.contrib import admin
##from guardian import 

from . import models


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name','title',)
    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','blog','author','title','published','created')
    

admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Article, ArticleAdmin)
