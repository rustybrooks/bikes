# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1474419289.824691
_enable_loop = True
_template_filename = u'/home/rbrooks/programs/bike/bikething/templates/bikecal/base.html'
_template_uri = u'bikecal/base.html'
_source_encoding = 'ascii'
_exports = [u'header', u'head', u'footer']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def header():
            return render_header(context._locals(__M_locals))
        def head():
            return render_head(context._locals(__M_locals))
        self = context.get('self', UNDEFINED)
        def footer():
            return render_footer(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'<html>\n<head>\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'head'):
            context['self'].head(**pageargs)
        

        __M_writer(u'\n</head>\n\n<body>\n<div class="header">\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        __M_writer(u'\n</div>\n\n    ')
        __M_writer(unicode(self.body()))
        __M_writer(u'\n\n<div class="footer">\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'footer'):
            context['self'].footer(**pageargs)
        

        __M_writer(u'\n</div>\n\n</body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def header():
            return render_header(context)
        __M_writer = context.writer()
        __M_writer(u'\n        this is the header\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def head():
            return render_head(context)
        __M_writer = context.writer()
        __M_writer(u'\n        <link rel="StyleSheet" href="/static/bikecal/style.css" type="text/css" media="screen">\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def footer():
            return render_footer(context)
        __M_writer = context.writer()
        __M_writer(u'\n        <div class="copyright" style="text-align: right;" >\n            <p>\n                Copyright Rusty Brooks 2014-Present\n        </div>\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"33": 5, "69": 3, "38": 12, "39": 15, "40": 15, "75": 18, "45": 23, "16": 0, "81": 18, "51": 10, "87": 81, "57": 10, "28": 1, "63": 3}, "uri": "bikecal/base.html", "filename": "/home/rbrooks/programs/bike/bikething/templates/bikecal/base.html"}
__M_END_METADATA
"""
