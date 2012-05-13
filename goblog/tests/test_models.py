import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone as djtimezone

from goblog import models, errors

from . import base

#==============================================================================#
class Article_TestCase(base.DBTestCaseBase):
    def setUp(self):
        super(Article_TestCase, self).setUp()
        self.blogname = 'myblog'
        self.blogtitle = 'My Blog!'
        self.blog = models.Blog(name=self.blogname, title=self.blogtitle)
        self.blog.save()
        self.username = 'TheAuthor'
        self.email = 'theauthor@example.com'
        self.password = 'password'
        self.author = User.objects.create_user(self.username, self.email, self.password)
        self.author.save()
        
    def test_clean_notreadonly(self):
        id = 'MyArticle'
        title = 'My Article Title'
        
        self.assertEqual(0, models.Article.objects.count())
        article = models.Article(blog=self.blog, id=id, author=self.author, title=title)
        article.clean()  # no exceptions
        article.save()
        
        self.assertEqual(1, models.Article.objects.count())
        
        article = models.Article.objects.get(id=id)
        title2 = 'A Better Article Title'
        article.title = title2  # title attribute is not readonly
        article.clean()  # no exceptions
        article.save()
        
        self.assertEqual(title2, models.Article.objects.get(id=id).title)
        
    def test_clean_readonly(self):
        id = 'MyArticle'
        title = 'My Article Title'
        
        self.assertEqual(0, models.Article.objects.count())
        article = models.Article(blog=self.blog, id=id, author=self.author, title=title)
        article.clean()  # no exceptions
        article.save()
        
        self.assertEqual(1, models.Article.objects.count())
        
        now = djtimezone.now()
        article = models.Article.objects.get(id=id)
        article.created = now  # created attribute is readonly
        
        with self.assertRaises(ValidationError):
            article.clean()
        

#==============================================================================#
