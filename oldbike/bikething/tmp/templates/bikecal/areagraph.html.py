# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1474666870.552825
_enable_loop = True
_template_filename = '/home/rbrooks/programs/bike/bikething/templates/bikecal/areagraph.html'
_template_uri = 'bikecal/areagraph.html'
_source_encoding = 'ascii'
_exports = [u'header']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        series = context.get('series', UNDEFINED)
        yaxis_label = context.get('yaxis_label', UNDEFINED)
        graph_title = context.get('graph_title', UNDEFINED)
        json_keys = context.get('json_keys', UNDEFINED)
        def header():
            return render_header(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n\n<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n\n<script type="text/javascript">\n$(function () {\n    $(\'#container\').highcharts({\n        chart: {\n            type: \'area\'\n        },\n        title: {\n            text: \'')
        __M_writer(unicode(graph_title))
        __M_writer(u"'\n        },\n        subtitle: {\n            text: ''\n        },\n        xAxis: {\n            allowDecimals: false,\n            labels: {\n                formatter: function () {\n                    return this.value; // clean, unformatted number for year\n                }\n            },\n            'categories': ")
        __M_writer(unicode(json_keys))
        __M_writer(u"\n        },\n        yAxis: {\n            title: {\n                text: '")
        __M_writer(unicode(yaxis_label))
        __M_writer(u"'\n            },\n            labels: {\n                formatter: function () {\n                    return this.value;\n                }\n            }\n        },\n\n        plotOptions: {\n            area: {\n                pointStart: 0,\n                marker: {\n                    enabled: false,\n                    symbol: 'circle',\n                    radius: 2,\n                    states: {\n                        hover: {\n                            enabled: true\n                        }\n                    }\n                }\n            }\n        },\n        series: ")
        __M_writer(unicode(series))
        __M_writer(u'\n    });\n});\n</script>\n\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        __M_writer(u'\n\n<script src="/static/bikecal/highcharts/js/highcharts.js"></script>\n<script src="/static/bikecal/highcharts/js/modules/exporting.js"></script>\n\n<div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def header():
            return render_header(context)
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"69": 63, "38": 1, "39": 12, "40": 12, "41": 24, "42": 24, "43": 28, "44": 28, "45": 52, "46": 52, "51": 59, "57": 58, "27": 0, "63": 58}, "uri": "bikecal/areagraph.html", "filename": "/home/rbrooks/programs/bike/bikething/templates/bikecal/areagraph.html"}
__M_END_METADATA
"""
