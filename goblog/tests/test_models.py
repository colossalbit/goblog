from goblog import models, errors

from . import base

class Blog_TestCase(base.DBTestCaseBase):
    def setUp(self):
        super(Blog_TestCase, self).setUp()
        self.blogspacename = 'blogspace'
        self.blogspace = models.BlogSpace(name=self.blogspacename)
        self.blogspace.save()
        
    def test_save_notreadonly(self):
        name = 'MyBlog'
        title = 'My Blog Title'
        
        self.assertEqual(0, models.Blog.objects.count())
        blog = models.Blog(blogspace=self.blogspace, name=name, title=title)
        blog.save()
        
        self.assertEqual(1, models.Blog.objects.count())
        
        blog = models.Blog.objects.get(name=name)
        title2 = 'A Better Blog Title'
        blog.title = title2  # title attribute is not readonly
        blog.save()
        
        self.assertEqual(title2, models.Blog.objects.get(name=name).title)
        
    def test_save_readonly(self):
        name = 'MyBlog'
        title = 'My Blog Title'
        
        self.assertEqual(0, models.Blog.objects.count())
        blog = models.Blog(blogspace=self.blogspace, name=name, title=title)
        blog.save()
        
        self.assertEqual(1, models.Blog.objects.count())
        
        blogspace2 = models.BlogSpace(name='blogspace2')
        blogspace2.save()
        blog = models.Blog.objects.get(name=name)
        blog.blogspace = blogspace2  # blogspace attribute is readonly
        
        with self.assertRaises(errors.GoBlogError):
            blog.save()
        

