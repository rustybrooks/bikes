# Fundamentals
from django.http import HttpResponse
from django.conf import settings

#things we need to overwrite are imported here
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Template, RequestContext


from mako import exceptions

# Templating
from template import TemplateHelper


#render to string, render to response
def wrap_function(fun):
    def wrapper(*args, **kwargs):
        save_globals = fun.func_globals.copy()
        
        to_overwrite = {render_to_response:_overwrite_render_to_response,
                        render_to_string:_overwrite_render_to_string,
                        Template:_OverwriteTemplate,
                        RequestContext:_OverwriteRequestContext}
        
        overwritten_keys = []
        
        #this should work for any objects directly imported under any name,
        #although it won't work for objects accessed by importing their module
        for key, value in fun.func_globals.iteritems():
            try:
                if value in to_overwrite:
                    fun.func_globals[key] = to_overwrite[value]
                    overwritten_keys.append(key)
            except TypeError:
                #whoops, that guy wasn't hashable!
                continue
        
        ret = fun(*args, **kwargs)
        
        #and set these back so we haven't changed the behavior of the function
        #elsewhere, in case that turns out to matter.
        for key in overwritten_keys:
            fun.func_globals[key] = save_globals[key]
            
        return ret
    return wrapper

def _overwrite_render_to_string(template_name, dictionary={}, context_instance=None):
    return _grab_mako_template(template_name, dictionary, context_instance)

def _overwrite_render_to_response(template, dictionary={}, context_instance=None, mimetype=settings.DEFAULT_CONTENT_TYPE):
    response = HttpResponse()
    response.content = _grab_mako_template(template, dictionary, context_instance)
    return response
    #print 'called my awesome rendering dude thing!'
    
def _grab_mako_template(template_name, dictionary, context_instance):
    request = False
    context = {'page_title':''}
    
    if context_instance:
        request = context_instance.request
        context.update(context_instance.dict_)
    
    context.update(dictionary)
    
    #print context
    
    if not isinstance(template_name, str):
        #list of templates passed in, try in order until we find one
        for name in template_name:
            try:
                temp = TemplateHelper(name, request, context)
                break
            except exceptions.TopLevelLookupException:
                pass
    else:
        temp = TemplateHelper(template_name, request, context)
        
    return temp.render()

class _OverwriteTemplate(object):
    pass

class _OverwriteRequestContext(object):
    
    def __init__(self, request, dict=None, processors=None, current_app=None):
        self.request = request
        self.dict_ = dict or {}
