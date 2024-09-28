import UserDict

from django.template import Token, TOKEN_BLOCK
#from mako.template import Template
#from mako.runtime import Context


class _DummyParser(object):
    """
    A dummy parser class for passing to django template tag parsers when what
    we're actually rendering is a mako template.
    """

    def __init__(self, context):
        self.context = context
        
        #could add all my default libraries here.
        #for lib in builtins:
        #    self.add_library(lib)

    def parse(self, parse_until=None):
        raise NotImplementedError("Dummy mako parser parse can't really parse parser!")
        

    def skip_past(self, endtag):
        raise NotImplementedError("Dummy mako skip_past not implemented!")

    def delete_first_token(self):
        """
        This is called in order to handle block-ending tags, and those should
        not be called in the 'normal' way.
        """
        raise NotImplementedError("Dummy mako delete_first_token not implemented!")

    def add_library(self, lib):
        self.context['django_tags'].update(lib.tags)

    def compile_filter(self, token):
        """
        
        """
        #so I need to take a look at this, but what I actually want to do is
        #basically keep this as python code, instead of template code, and have
        #'resolve' run it appropriately...
        return _DummyFilterExp(token, self)
#    
#    I doubt I'll need this, but keeping it around just in case
#    def find_filter(self, filter_name):
#        if filter_name in self.filters:
#            return self.filters[filter_name]
#        else:
#            raise TemplateSyntaxError("Invalid filter: '%s'" % filter_name)


#it *may* be reasonable to compact these into one thing...
class _DummyFilterExp(object):
    """
    A dummy filter expression used to bypass django's tagging system filter
    processing. Because, like, ew. 
    """
    def __init__(self, token, parser):
        #token inputs here look like, eg, user.id|a|b|c
        #so.... this should be made more robust :)
        #print token
        self.var = _DummyVariable(token)
        
        
    def resolve(self, context, ignore_failures=False):
        '''
        
        from mako.template import Template

        template = Template("""
            <%def name="hi(name)">
                hi ${name}!
            </%def>
        
            <%def name="bye(name)">
                bye ${name}!
            </%def>
        """)
        
        print template.get_def("hi").render(name="ed")
        print template.get_def("bye").render(name="ed")
        '''
        #so I *think* what this needs to do is return a dummy variable object
        #that hooks into the appropriate mako variable. Whee.
        return self.var.resolve(context)
    
class _DummyVariable(object):
    """
    A dummy variable used to bypass django's tagging system variable processing
    because ew gross.
    """
    
    def __init__(self, varname):
        self.varname = varname
        
    def resolve(self, context):
        #whee.
        try:
            return context[self.varname]
        except KeyError:
            return self.varname
    
class _DummyContext(UserDict.DictMixin):
    """
    Little extension to Context object that lets us define new local variables,
    which I think is the right thing to do.
    """
    def __init__(self, context):
        self.context = context
        
    def __getitem__(self, key):
        return self.context[key]
        
    def __setitem__(self, key, val):
        self.context._data[key] = val
        
    def __delitem__(self, key):
        #let's not allow willy-nilly deletion from the context, kay?
        pass
    
    #what I should really do is implement a general 'if you call something I
    #don't know the name of, try calling it on context
    def keys(self):
        return self.context.keys()
    
    #some dummy functions that some tags call.
    def push(self):
        pass
    
    def pop(self):
        pass
    
    def autoescape(self):
        return self.context.autoescape()
    
    def current_app(self):
        return self.context.current_app()
    
def tag(context, tag_name, tag_params=None):
    """
    try:
        compile_func = self.context.<tag_function>
    except KeyError:
        #explode
    result = compile_func(self, a_token)
    self.context.<tag_runner_thing> = result.render(context)
    
    """
    #keys = context.keys()
    #keys.sort()
    #print keys
       # print context['waffles']
    try:
        compile_func = context['django_tags'][tag_name]
    except KeyError:
        raise KeyError(tag_name + ' not loaded into the current template!')
    
        #we should explode appropriately here
    compiled_node = compile_func(_DummyParser(context), Token(TOKEN_BLOCK, ' '.join([tag_name, tag_params])))
    res = compiled_node.render(_DummyContext(context))
    
    return res

def _create_mako_filter(filter_func):
    """
    So this is to make filters that take arguments. Whee!
    """
    
    if getattr(filter_func, '_decorated_function', filter_func).func_code.co_argcount == 1:
        return filter_func
    else:
        def filt(*arg):
            def do_filter(input=None):
                return filter_func(input, *arg)
            return do_filter
        filt.raw = filter_func
        filt.func_defaults = filter_func.func_defaults
        return filt
    

    
        
