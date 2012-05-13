from django import forms
from django.utils import timezone as djtimezone

from . import appsettings, validators


class ArticleFormBase(forms.Form):
    title = forms.CharField()
    published = forms.DateTimeField(required=False)
    compiler_name = forms.CharField(required=False, 
                                initial=appsettings.ARTICLE_COMPILER_DEFAULT, 
                                validators=[validators.validate_article_compiler])
    text = forms.CharField(widget=forms.Textarea)
    
    ##full = forms.TextField(required=False, widget=forms.HiddenInput)
    ##brief = forms.TextField(required=False, widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.do_compile = kwargs.pop('do_compile', True)
        super(ArticleFormBase, self).__init__(*args, **kwargs)
        self.article_full = ''
        self.article_brief = ''
        
    def clean_compiler_name(self):
        name = self.cleaned_data['compiler_name']
        if not name:
            name = appsettings.ARTICLE_COMPILER_DEFAULT
        return name
    
    def clean(self):
        cleaned_data = super(ArticleFormBase, self).clean()
        if self.do_compile and 'text' in cleaned_data and 'compiler_name' in cleaned_data:
            raw = cleaned_data['text']
            compiler_name = cleaned_data['compiler_name']
            from .core.articlecompilers import compile
            # TODO: translate compilation errors into ValidationErrors
            full, brief = compile(compiler_name, raw)
            self.article_full = full
            self.article_brief = brief
        return cleaned_data


class ArticleCreateForm(ArticleFormBase):
    ##blog      # blog may be implicit based on URL, or it may be explicit
    ##author    # author should be implict based on logged-in user
    ##created
    
    def clean_published(self):
        date = self.cleaned_data['published']
        now = djtimezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date and date < djtimezone.now():
            raise forms.ValidationError('Cannot set published date before today.')
        return date
    
    
class ArticleEditForm(ArticleFormBase):
    pass




