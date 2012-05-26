from django import template
from django.contrib.auth.models import User
from django.template.defaulttags import kwarg_re
from django.utils.encoding import smart_str

from .. import models, utils

register = template.Library()

#==============================================================================#
class CanEditArticleNode(template.Node):
    def __init__(self, user_str, article_str, context_var):
        self.user_var = template.Variable(user_str)
        self.article_var = template.Variable(article_str)
        self.context_var = context_var
        
    def render(self, context):
        try:
            user = self.user_var.resolve(context)
            article = self.article_var.resolve(context)
        except template.VariableDoesNotExist:
            context[self.context_var] = False
            return ''
        if not isinstance(user, User):
            context[self.context_var] = False
            return ''
        if not isinstance(article, models.Article):
            context[self.context_var] = False
            return ''
        r = article.user_can_edit_article(user)
        context[self.context_var] = r
        return ''


@register.tag
def goblog_can_edit_article(parser, token):
    # syntax: goblog_can_edit_article user article as "variable"
    bits = token.split_contents()
    format = '{% goblog_can_edit_article user article as "context_var" %}'
    if len(bits) != 5 or bits[3] != 'as':
        raise template.TemplateSyntaxError("goblog_can_edit_article "
            "tag should be in format: {0}".format(format))
    user = bits[1]
    article = bits[2]
    context_var = bits[4]
    if context_var[0] != context_var[-1] or context_var[0] not in ('"', "'"):
        raise template.TemplateSyntaxError("goblog_can_edit_article tag's "
            "context_var argument should be in quotes")
    context_var = context_var[1:-1]
    return CanEditArticleNode(user, article, context_var)
    
#==============================================================================#
class BlogUrlNode(template.Node):
    def __init__(self, viewname, blogid, args, kwargs, asvar):
        self.viewname = viewname
        self.blogid = blogid
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        viewname = self.viewname.resolve(context)
        blogid = self.blogid.resolve(context)
        
        url = utils.reverse_blog_url(viewname, blogid, args=args, kwargs=kwargs)
        return url
            
            
@register.tag
def goblog_blogurl(parser, token):
    # syntax: goblog_blogurl VIEWNAME BLOGID arg1 arg2 kwarg1=val1 kwarg2=val2
    bits = token.split_contents()
    format = '{% goblog_blogurl VIEWNAME BLOGID [arg ...] [kwarg=val ...] %}'
    if len(bits) < 3:
        raise template.TemplateSyntaxError("goblog_blogurl "
            "tag should be in format: {0}".format(format))
    viewname = parser.compile_filter(bits[1])
    blogid = parser.compile_filter(bits[2])
    args = []
    kwargs = {}
    asvar = None
    
    bits = bits[3:]
    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise template.TemplateSyntaxError("Malformed arguments to goblog_blogurl tag")
        name, value = match.groups()
        if name:
            kwargs[name] = parser.compile_filter(value)
        else:
            args.append(parser.compile_filter(value))

    return BlogUrlNode(viewname, blogid, args, kwargs, asvar)
    

#==============================================================================#

