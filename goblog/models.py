import datetime

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import timezone as djtimezone

from . import errors, appsettings


# Extra User attributes:
#   - timezone (to localize time displays)
#   - incorporate OpenID information?
#   - show username, first and last name, other?


# Use this DefaultBlog model, or use a setting GOBLOG_DEFAULT_BLOG?
##class DefaultBlog(models.Model):
##    site =          models.ForeignKey(Site, unique=True)
##    defaultblog =   models.ForeignKey('Blog')

#==============================================================================#
def datetime_now():
    return djtimezone.now()


def _check_read_only(instance, fields):
    if isinstance(fields, basestring):
        fields = (fields,)
    try:
        obj = instance.__class__.objects.only(*fields).get(pk=instance.pk)
        for field in fields:
            if not getattr(obj, field) == getattr(instance, field):
                m = "Cannot modify field '{0}', it is read-only.".format(field)
                raise ValidationError(m)
    except ObjectDoesNotExist:
        pass


##class BlogSpace(models.Model):
##    name = models.CharField(max_length=appsettings.BLOGSPACE_NAME_MAXLEN)


#==============================================================================#
class Blog(models.Model):
    """A blog."""
    ##id =        models.CharField(max_length=32, primary_key=True)
    # The name is used in the URL.
    name =      models.SlugField(max_length=appsettings.BLOG_NAME_MAXLEN, 
                                 primary_key=True)
    title =     models.TextField()
    ##blogspace = models.ForeignKey(BlogSpace)
    ##created =   models.DateTimeField(default=datetime_now)
    # To sort by most recently updated: sort on max(created, self.articles.get(max(published)))
    ##theme =     models.CharField(max_length=100, blank=True)
    # TODO: Other blog level info here... 
    # TODO: site? language? default timezone?
    # TODO: option to disable localizing time displays?
    
    class Meta(object):
        permissions = (
            ('create_article','Create article'),
        )
    
    def __unicode__(self):
        return self.name
        
    def clean(self):
        super(Blog, self).clean()
    
    def save(self, *args, **kwargs):
        ##_check_read_only(self, ('name',))
        super(Blog, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('goblog-blog-main', (), {'blogid': self.name})
        
    def user_can_create_article(self, user):
        if user.is_superuser:
            return True
        elif user.has_perm('goblog.create_article', self):
            return True
        return False
        
    def user_can_edit_blog(self, user):
        if user.is_superuser:
            return True
        elif user.has_perm('goblog.change_blog', self):
            return True
        return False
    

#==============================================================================#
class Article(models.Model):
    """An article in a blog."""
    id =            models.CharField(max_length=appsettings.ARTICLE_NAME_MAXLEN, 
                                     primary_key=True)
    blog =          models.ForeignKey(Blog, related_name='articles')
    author =        models.ForeignKey(User, related_name='+')
    title =         models.TextField()
    published =     models.DateTimeField(null=True, default=None, blank=True)
    # should default to the blog's theme
    ##theme =         models.CharField(max_length=100, blank=True)
    created =       models.DateTimeField(default=datetime_now, editable=False)
    
    # Changing the compiler of an existing article should require the article 
    # be recompiled with the new compiler *before* saving the change.
    compiler_name = models.CharField(
                            choices=appsettings.ARTICLE_COMPILER_CHOICES,
                            max_length=appsettings.ARTICLE_COMPILER_MAXLEN,
                            default=appsettings.GOBLOG_ARTICLE_COMPILER_DEFAULT)
    
    # Do not show in various lists, such as recently modified articles. Useful 
    # for non-article pages such as "about" or "links".
    ##nolist =        models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'{0} -- "{1}"'.format(self.id, self.title)
        
    def clean(self):
        super(Article, self).clean()
        _check_read_only(self, ('blog','author','created',))
        ##try:
        ##    obj = Article.objects.only('published').get(pk=self.pk)
        ##    if obj.published is not None and obj.published != self.published:
        ##        raise ValidationError('The published date cannot be changed.')
        ##except ObjectDoesNotExist:
        ##    pass
    
    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ('goblog-article-view', (), {'blogid': self.blog_id, 'articleid': self.id})
        
    def user_can_edit_article(self, user):
        if user.is_superuser:
            return True
        elif self.author == user:
            return True
        elif user.has_perm('goblog.change_article', self):
            return True
        return False
    
    
class ArticleEdit(models.Model):
    """Describes an edit on an article.  
    
    Note: This is *not* intended to record the actual changes to the content.
    It simply records who edited it and when.
    """
    article =       models.ForeignKey(Article, related_name='edits', 
                                      editable=False)
    editor =        models.ForeignKey(User, related_name='+', editable=False)
    date =          models.DateTimeField(default=datetime_now, editable=False)
    
    def clean(self):
        super(ArticleEdit, self).clean()
        _check_read_only(self, ('article','editor','date',))
    
    def save(self, *args, **kwargs):
        super(ArticleEdit, self).save(*args, **kwargs)
    
    
class ArticleContent(models.Model):
    """Contains the article's content. These fields could have been a part of 
    'Article' itself, but instead are separated for performance reasons.
    """
    article =       models.OneToOneField(Article, related_name='content', 
                                         editable=True)
    raw =           models.TextField()
    text_start =    models.TextField(blank=True, editable=False)
    text_end =      models.TextField(blank=True, editable=False)
    ##full =          models.TextField(blank=True, editable=False)
    # The brief is shown on the front page and in other summaries. If blank, 
    # 'full' is used.
    ##brief =         models.TextField(blank=True, editable=False)
    
    def clean(self):
        super(ArticleContent, self).clean()
        _check_read_only(self, ('article',))
        # set 'text_start' and 'text_end'
        if self.raw:
            from .core.articlecompilers import compile, resolve_article_compiler
            dotted_name = resolve_article_compiler(self.article.compiler_name)
            start, end = compile(dotted_name, self.raw)
            self.text_start = start
            self.text_end = end
        else:
            self.text_start = ''
            self.text_end = ''
    
    def save(self, *args, **kwargs):
        super(ArticleContent, self).save(*args, **kwargs)

    
#==============================================================================#
    
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



