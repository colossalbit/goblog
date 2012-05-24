from django import template
from django.contrib.auth.models import User

from .. import models

register = template.Library()

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
    # goblog_can_edit_article user article as "variable"
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
    


