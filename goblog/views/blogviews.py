from django.views.generic.detail import DetailView

from .. import models


class BlogMainView(DetailView):
    model = models.Blog
    slug_field = 'name'
    slug_url_kwarg = 'blogid'
    context_object_name = 'blog'
    template_name = 'goblog/blogmain.html'

