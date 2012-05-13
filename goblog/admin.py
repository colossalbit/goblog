from django.contrib import admin
from django import forms
##from guardian import 

from . import models


# class BlogAdminForm(forms.ModelForm):
    # class Meta:
        # model = models.Blog

    # def clean(self):
        # super(BlogAdminForm, self).clean()
        
        # return self.cleaned_data["name"]


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'title',)
    
    fields = ('name', 'title',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['name']
    

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'author', 'title', 'published', 'created', 'compiler_name',)
    
    fields = ('id', 'blog', 'author', 'title', 'published','compiler_name',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['created',]
        else:
            return ['id','blog','created',]
    

class ArticleEditAdmin(admin.ModelAdmin):
    list_display = ('article', 'editor', 'date',)
    

class ArticleContentAdmin(admin.ModelAdmin):
    list_display = ('article', 'raw', 'full', 'brief',)
    
    fields = ('article', 'raw',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['article',]
    

admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleEdit, ArticleEditAdmin)
admin.site.register(models.ArticleContent, ArticleContentAdmin)
