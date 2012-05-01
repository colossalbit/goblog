import datetime

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from . import errors, appsettings


# Extra User attributes:
#   - timezone (to localize time displays)
#   - incorporate OpenID information?


# Use this DefaultBlog model, or use a setting GOBLOG_DEFAULT_BLOG?
##class DefaultBlog(models.Model):
##    site =          models.ForeignKey(Site, unique=True)
##    defaultblog =   models.ForeignKey('Blog')


def _check_read_only(instance, fields):
    if isinstance(fields, basestring):
        fields = (fields,)
    try:
        obj = instance.__class__.objects.only(*fields).get(pk=instance.pk)
        for field in fields:
            if not getattr(obj, field) == getattr(instance, field):
                raise errors.GoBlogError()
    except ObjectDoesNotExist:
        pass


##class BlogSpace(models.Model):
##    name = models.CharField(max_length=appsettings.BLOGSPACE_NAME_MAXLEN)


class Blog(models.Model):
    """A blog."""
    ##id =        models.CharField(max_length=32, primary_key=True)
    name =      models.CharField(max_length=appsettings.BLOG_NAME_MAXLEN, primary_key=True)  # used in URL
    title =     models.TextField()
    ##blogspace = models.ForeignKey(BlogSpace)
    ##created =   models.DateTimeField(default=datetime.datetime.now)
    # To sort by most recently updated: sort on max(created, self.articles.get(max(published)))
    ##theme =     models.CharField(max_length=100, blank=True)
    # TODO: Other blog level info here... 
    # TODO: site? language? default timezone?
    # TODO: option to disable localizing time displays?
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        _check_read_only(self, ('name',))
        super(Blog, self).save(*args, **kwargs)
    

class Article(models.Model):
    """An article in a blog."""
    id =            models.CharField(max_length=appsettings.ARTICLE_NAME_MAXLEN, primary_key=True)
    blog =          models.ForeignKey(Blog, related_name='articles')
    author =        models.ForeignKey(User, related_name='+')
    title =         models.TextField()
    published =     models.DateTimeField(null=True, default=None)
    # should default to the blog's theme
    ##theme =         models.CharField(max_length=100, blank=True)
    created =       models.DateTimeField(default=datetime.datetime.now)
    # Do not show in various lists, such as recently modified articles. Useful 
    # for non-article pages such as "about" or "links".
    ##nolist =        models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        _check_read_only(self, ('blog','author','created',))
        try:
            obj = Article.objects.only(*fields).get(pk=self.pk)
            if obj.published is not None and obj.published != self.published:
                raise errors.GoBlogError()
        except ObjectDoesNotExist:
            pass
        super(Article, self).save(*args, **kwargs)
    
    
class ArticleEdit(models.Model):
    """Describes an edit on an article.  
    
    Note: This is *not* intended to record the actual changes to the content.
    It simply records who edited it and when.
    """
    article =       models.ForeignKey(Article, related_name='edits')
    editor =        models.ForeignKey(User, related_name='+')
    date =          models.DateTimeField(default=datetime.datetime.now)
    
    def save(self, *args, **kwargs):
        _check_read_only(self, ('article','editor','date',))
        super(ArticleEdit, self).save(*args, **kwargs)
    
    
class ArticleContent(models.Model):
    """Contains the article's content. These fields could have been a part of 
    'Article' itself, but instead are separated for performance reasons.
    """
    article =       models.OneToOneField(Article, related_name='content')
    raw =           models.TextField()
    full =          models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        try:
            obj = ArticleContent.objects.only('article').get(pk=self.pk)
            if not obj.article == self.article:
                raise errors.GoBlogError()
        except ObjectDoesNotExist:
            pass
        super(ArticleContent, self).save(*args, **kwargs)

    
    
##class Tag(models.Model):
##    """Tag that can be added to an article.  Tags are specific to a tagspace."""
##    blogspace =     models.ForeignKey(TagSpace)
##    articles =      models.ManyToManyField(Article, related_name='tags', through=)
##    name =          models.CharField(max_length=100)
##    description =   models.TextField()
##    created =       models.DateTimeField(default=datetime.datetime.now)
    
    
##class TaggedBy(models.Model):
##    tag = models.ForeignKey(Tag)
##    article = models.ForeignKey(Article)
##    
##    def clean(self):
##        if tag.tagspace != article.blog.tagspace:
##            raise ValidationError('Articles and their Tags must belong to the same TagSpace.')
    
    
##class Comment(models.Model):
##    """A comment on an article."""
##    article =       models.ForeignKey(Article, related_name='comments')
##    parent =        models.ForeignKey('self', null=True, related_name='responses')
##    # either 'user' is required or both 'username' and 'email' are required.
##    user =          models.ForeignKey(User, related_name='+', null=True)
##    username =      models.CharField(max_length=100)
##    email =         models.EmailField(max_length=254)
##    ipaddress =     models.IPAddressField()
##    subject =       models.CharField(max_length=100)
##    body =          models.TextField()
##    date =          models.DateTimeField()
##    modified =      models.DateTimeField(null=True, default=None)
##    # if comments are moderated, this controls whether the comment is displayed
##    approved =      models.NullBooleanField(default=None)



