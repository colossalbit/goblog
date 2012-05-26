import warnings
import datetime

from django.core.urlresolvers import reverse as urlreverse
from django.utils import timezone as djtimezone

from goblog.views import blogviews
from . import base

#==============================================================================#
class View_TestCaseBase(base.TestCaseBase):
    now = datetime.datetime(2012,5,30, 0,0,0, tzinfo=djtimezone.utc)
    
    def setUp(self):
        super(View_TestCaseBase, self).setUp()
        self._oldnow = blogviews.GoBlogMixin.now
        blogviews.GoBlogMixin.now = self.now
        
    def tearDown(self):
        blogviews.GoBlogMixin.now = self._oldnow
        super(View_TestCaseBase, self).tearDown()


#==============================================================================#
class BlogView_TestCase(View_TestCaseBase):
    fixtures = ['goblog/tests/superuser.yaml', 'goblog/tests/blog1.yaml']
    
    def test_anonymous_user(self):
        blogid = 'blog1'
        url = urlreverse('goblog-blog-main', kwargs={'blogid': blogid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(200, response.status_code)
        self.assertTrue('LOGIN_URL' in context)
        self.assertTrue('LOGOUT_URL' in context)
        self.assertTrue('LOGIN_REDIRECT_URL' in context)
        self.assertTrue('LOGOUT_REDIRECT_URL' in context)
        
        # anonymous user, so login link should be available
        self.assertTrue(context['LOGIN_URL'] in body)
        # anonymous user, so no logout link should be available
        self.assertTrue(context['LOGOUT_URL'] not in body)
        self.assertEqual(url, context['LOGIN_REDIRECT_URL'])
        
        # create article link should not appear
        createurl = urlreverse('goblog-article-create', 
                               kwargs={'blogid': blogid})
        self.assertTrue(createurl not in body)
        
        # no edit links should appear
        edit1url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article1'})
        self.assertTrue(edit1url not in body)
        edit2url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article2'})
        self.assertTrue(edit2url not in body)
        edit3url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article3'})
        self.assertTrue(edit3url not in body)
        
        # links to published articles should appear
        view2url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article2'})
        self.assertTrue(view2url in body)
        view3url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article3'})
        self.assertTrue(view3url in body)
        
        # links to unpublished articles should *not* appear
        view1url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article1'})
        self.assertTrue(view1url not in body)
    
    def test_super_user(self):
        blogid = 'blog1'
        url = urlreverse('goblog-blog-main', kwargs={'blogid': blogid})
        self.client.login(username='superuser', password='nothing')
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(200, response.status_code)
        self.assertTrue('LOGIN_URL' in context)
        self.assertTrue('LOGOUT_URL' in context)
        self.assertTrue('LOGIN_REDIRECT_URL' in context)
        self.assertTrue('LOGOUT_REDIRECT_URL' in context)
        
        # logged-in user, so login link should not be available
        self.assertTrue(context['LOGIN_URL'] not in body)
        # logged-in user, so logout link should be available
        self.assertTrue(context['LOGOUT_URL'] in body)
        self.assertEqual(url, context['LOGIN_REDIRECT_URL'])
        
        # create article link should appear
        createurl = urlreverse('goblog-article-create', 
                               kwargs={'blogid': blogid})
        self.assertTrue(createurl in body)
        
        # unpublished edit links should not appear
        edit1url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article1'})
        self.assertTrue(edit1url not in body)
        
        # published edit links should appear
        edit2url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article2'})
        self.assertTrue(edit2url in body)
        edit3url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article3'})
        self.assertTrue(edit3url in body)
        
        # links to published articles should appear
        view2url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article2'})
        self.assertTrue(view2url in body)
        view3url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article3'})
        self.assertTrue(view3url in body)
        
        # links to unpublished articles should *not* appear
        view1url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                'articleid': 'blog1article1'})
        self.assertTrue(view1url not in body)
        
    def test_unknown_blog(self):
        blogid = 'not_a_known_blog'
        url = urlreverse('goblog-blog-main', kwargs={'blogid': blogid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(404, response.status_code)
        

#==============================================================================#
class ArticleView_TestCase(View_TestCaseBase):
    fixtures = ['goblog/tests/superuser.yaml', 'goblog/tests/blog1.yaml']
    
    def test_anonymous_user(self):
        blogid = 'blog1'
        articleid = 'blog1article2'
        url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                        'articleid': articleid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(200, response.status_code)
        self.assertTrue('LOGIN_URL' in context)
        self.assertTrue('LOGOUT_URL' in context)
        self.assertTrue('LOGIN_REDIRECT_URL' in context)
        self.assertTrue('LOGOUT_REDIRECT_URL' in context)
        
        # anonymous user, so login link should be available
        self.assertTrue(context['LOGIN_URL'] in body)
        # anonymous user, so no logout link should be available
        self.assertTrue(context['LOGOUT_URL'] not in body)
        self.assertEqual(url, context['LOGIN_REDIRECT_URL'])
        
        # TODO: no edit links should appear
    
    def test_anonymous_user_and_unpublished_article(self):
        blogid = 'blog1'
        articleid = 'blog1article1'  # article is unpublished
        url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                        'articleid': articleid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(404, response.status_code)
    
    def test_super_user_and_unpublished_article(self):
        blogid = 'blog1'
        articleid = 'blog1article1'  # article is unpublished
        url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                        'articleid': articleid})
        self.client.login(username='superuser', password='nothing')
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(200, response.status_code)
        
        # logged-in user, so login link should not be available
        self.assertTrue(context['LOGIN_URL'] not in body)
        # logged-in user, so logout link should be available
        self.assertTrue(context['LOGOUT_URL'] in body)
        self.assertEqual(url, context['LOGIN_REDIRECT_URL'])
        
        # create article link should appear
        createurl = urlreverse('goblog-article-create', 
                               kwargs={'blogid': blogid})
        self.assertTrue(createurl in body)
        
    def test_unknown_blog(self):
        blogid = 'not_a_known_blog'
        articleid = 'blog1article2'
        url = urlreverse('goblog-article-view', kwargs={'blogid': blogid,
                                                        'articleid': articleid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(404, response.status_code)
        
    def test_unknown_article(self):
        blogid = 'blog1'
        articleid = 'not_a_known_article'
        url = urlreverse('goblog-article-view', kwargs={'blogid': blogid, 
                                                        'articleid': articleid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        self.assertEqual(404, response.status_code)
        

#==============================================================================#
class ArticleCreate_TestCase(View_TestCaseBase):
    fixtures = ['goblog/tests/superuser.yaml', 'goblog/tests/blog1.yaml']
    
    def test_anonymous_user(self):
        blogid = 'blog1'
        url = urlreverse('goblog-article-create', kwargs={'blogid': blogid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        # anonymous users cannot create articles
        self.assertEqual(403, response.status_code)
        
        # TODO: test anonymous user POSTing to view
        

#==============================================================================#
class ArticleEdit_TestCase(View_TestCaseBase):
    fixtures = ['goblog/tests/superuser.yaml', 'goblog/tests/blog1.yaml']
    
    def test_anonymous_user(self):
        blogid = 'blog1'
        articleid = 'blog1article1'
        url = urlreverse('goblog-article-edit', kwargs={'blogid': blogid, 
                                                        'articleid': articleid})
        response = self.client.get(url)
        context = response.context
        body = response.content
        # anonymous users cannot edit articles
        self.assertEqual(403, response.status_code)

        
#==============================================================================#

