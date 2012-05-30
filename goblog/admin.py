from django.contrib import admin
from django import forms

from guardian.admin import GuardedModelAdmin

from . import models


# class BlogAdminForm(forms.ModelForm):
    # class Meta:
        # model = models.Blog

    # def clean(self):
        # super(BlogAdminForm, self).clean()
        
        # return self.cleaned_data["name"]


class BlogAdmin(GuardedModelAdmin):
    list_display = ('name', 'title',)
    
    fields = ('name', 'title',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['name']
    

class ArticleAdmin(GuardedModelAdmin):
    list_display = ('id', 'blog', 'author', 'title', 'published', 'created', 'compiler_name',)
    
    fields = ('id', 'blog', 'author', 'title', 'published','compiler_name',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['created',]
        else:
            return ['id','blog','created',]
    
    def has_add_permission(self, request):
        return False
    

class ArticleEditAdmin(admin.ModelAdmin):
    list_display = ('article', 'editor', 'date',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.has_perm('goblog.change_article', obj.article)
        else:
            return request.user.has_perm('goblog.change_article')
    
    def has_delete_permission(self, request, obj=None):
        return False
    

class ArticleContentAdmin(admin.ModelAdmin):
    list_display = ('article', 'raw', 'brief', 'full',)
    
    fields = ('article', 'raw',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        else:
            return ['article',]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.has_perm('goblog.change_article', obj.article)
        else:
            return request.user.has_perm('goblog.change_article')
    
    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user.has_perm('goblog.delete_article', obj.article)
        else:
            return request.user.has_perm('goblog.delete_article')
    

admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleEdit, ArticleEditAdmin)
admin.site.register(models.ArticleContent, ArticleContentAdmin)
