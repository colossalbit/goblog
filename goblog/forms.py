from django import forms
from django.utils import timezone as djtimezone
from django.contrib.admin.widgets import AdminSplitDateTime

from . import appsettings, validators


class ArticleFormBase(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
    
    published = forms.SplitDateTimeField(required=False, 
                        widget=AdminSplitDateTime) #forms.DateTimeInput(attrs={'size': '40'}))
                        
    compiler_name = forms.ChoiceField(required=False, 
                            initial=appsettings.GOBLOG_ARTICLE_COMPILER_DEFAULT,
                            choices=appsettings.ARTICLE_COMPILER_CHOICES,
                            validators=[validators.validate_article_compiler],
                            widget=forms.Select(attrs={}))
                            
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '30'}))
    
    ##start = forms.TextField(required=False, widget=forms.HiddenInput)
    ##end = forms.TextField(required=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.do_compile = kwargs.pop('do_compile', True)
        super(ArticleFormBase, self).__init__(*args, **kwargs)
        self.article_start = ''
        self.article_end = ''
        
    def clean_compiler_name(self):
        name = self.cleaned_data['compiler_name']
        if not name:
            name = appsettings.GOBLOG_ARTICLE_COMPILER_DEFAULT
        return name
    
    def clean(self):
        cleaned_data = super(ArticleFormBase, self).clean()
        if self.do_compile and 'text' in cleaned_data and 'compiler_name' in cleaned_data:
            from .core.articlecompilers import compile, resolve_article_compiler
            raw = cleaned_data['text']
            compiler_name = cleaned_data['compiler_name']
            dotted_name = resolve_article_compiler(compiler_name)
            # TODO: translate compilation errors into ValidationErrors
            start, end = compile(dotted_name, raw)
            self.article_start = start
            self.article_end = end
        return cleaned_data


class ArticleCreateForm(ArticleFormBase):
    ##blog      # blog may be implicit based on URL, or it may be explicit
    ##author    # author should be implict based on logged-in user
    ##created
    
    def clean_published(self):
        date = self.cleaned_data['published']
        today = djtimezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date and date < today:
            raise forms.ValidationError('Cannot set published date before today.')
        return date
    
    
class ArticleEditForm(ArticleFormBase):
    # TODO: disallow published dates before created dates
    pass




