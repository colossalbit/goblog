from docutils.core import publish_parts

from . import base

#==============================================================================#
class ReStructuredTextArticleCompiler(base.ArticleCompiler):

    # Subclasses may use DOCUTILS_SETTINGS to customize Docutils' behavior.
    DOCUTILS_SETTINGS = {}
    
    # Options in DOCUTILS_SETTINGS_DEFAULTS are overridden by DOCUTILS_SETTINGS.
    DOCUTILS_SETTINGS_DEFAULTS = {
        'initial_header_level': '3',  # Lvl 1: page title, Lvl 2: article title
        'doctitle_xform': False,
    }
    
    # Options in DOCUTILS_SETTINGS_SECURE override options in DOCUTILS_SETTINGS 
    # and DOCUTILS_SETTINGS_DEFAULTS.
    DOCUTILS_SETTINGS_SECURE = {
        'fine_insertion_enabled': False,
        'raw_enabled': False,
    }
    
    def compile(self, text_start, text_end, target_element_id):
        settings_overrides = self.DOCUTILS_SETTINGS_DEFAULTS.copy()
        settings_overrides.update(self.DOCUTILS_SETTINGS)
        settings_overrides.update(self.DOCUTILS_SETTINGS_SECURE)
        
        # compile 'brief'
        parts1 = publish_parts(source=text_start, writer_name="html4css1", 
                               settings_overrides=settings_overrides)
        brief = parts1["fragment"]
        
        # compile 'full'
        if text_end:
            target = "\n\n.. _{0}:\n\n".format(target_element_id)
            full = ''.join((text_start, target, text_end))
            parts2 = publish_parts(source=full, writer_name="html4css1", 
                                   settings_overrides=settings_overrides)
            full = parts2["fragment"]
        else:
            full = ''
        
        return brief, full


#==============================================================================#

