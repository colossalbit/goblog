from django.utils import unittest

from goblog import models

class TestCaseBase(unittest.TestCase):
    pass
    
    
class DBTestCaseBase(TestCaseBase):
    def tearDown(self):
        models.ArticleEdit.objects.all().delete()
        models.ArticleContent.objects.all().delete()
        models.Article.objects.all().delete()
        models.Blog.objects.all().delete()
        models.BlogSpace.objects.all().delete()
        super(DBTestCaseBase, self).tearDown()
    
