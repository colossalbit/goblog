from django.utils import unittest
from django.test import TestCase as DjangoTestCase

from goblog import models

class TestCaseBase(DjangoTestCase):
    pass
    
    
class DBTestCaseBase(TestCaseBase):
    def ignore_tearDown(self):
        models.ArticleEdit.objects.all().delete()
        models.ArticleContent.objects.all().delete()
        models.Article.objects.all().delete()
        models.Blog.objects.all().delete()
        models.BlogSpace.objects.all().delete()
        super(DBTestCaseBase, self).tearDown()
    
