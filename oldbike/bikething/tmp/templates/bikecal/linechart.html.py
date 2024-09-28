# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1474667171.486442
_enable_loop = True
_template_filename = '/home/rbrooks/programs/bike/bikething/templates/bikecal/linechart.html'
_template_uri = 'bikecal/linechart.html'
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
        yaxis_max = context.get('yaxis_max', UNDEFINED)
        series = context.get('series', UNDEFINED)
        graph_title = context.get('graph_title', UNDEFINED)
        yaxis_min = context.get('yaxis_min', UNDEFINED)
        def header():
            return render_header(context._locals(__M_locals))
        __M_writer = context.writer()
        __M_writer(u'\n\n<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n\n<script type="text/javascript">\n    $(function () {\n    $(\'#container\').highcharts({\n        chart: {\n            type: \'spline\'\n        },\n        title: {\n            text: \'')
        __M_writer(unicode(graph_title))
        __M_writer(u"'\n        },\n        subtitle: {\n            text: ''\n        },\n        xAxis: {\n            //type: 'datetime',\n            //dateTimeLabelFormats: { // don't display the dummy year\n            //    month: '%e. %b',\n            //    year: '%b'\n            //},\n            title: {\n                text: 'Date'\n            }\n        },\n        yAxis: {\n            title: {\n                text: 'Snow depth (m)'\n            },\n            min: ")
        __M_writer(unicode(yaxis_min))
        __M_writer(u',\n            max: ')
        __M_writer(unicode(yaxis_max))
        __M_writer(u"\n        },\n        tooltip: {\n            headerFormat: '<b>{series.name}</b><br>',\n            pointFormat: '{point.x}: {point.y:.2f}'\n        },\n\n        plotOptions: {\n            spline: {\n                marker: {\n                    enabled: false\n                }\n            }\n        },\n\n        series: ")
        __M_writer(unicode(series))
        __M_writer(u'\n    });\n});\n</script>\n\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        __M_writer(u'\n\n<script src="/static/bikecal/highcharts/js/highcharts.js"></script>\n<script src="/static/bikecal/highcharts/js/modules/exporting.js"></script>\n\n<div id="container" style="min-width: 310px; height: 900px; margin: 0 auto"></div>')
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
{"source_encoding": "ascii", "line_map": {"69": 63, "38": 1, "39": 12, "40": 12, "41": 31, "42": 31, "43": 32, "44": 32, "45": 47, "46": 47, "51": 54, "57": 53, "27": 0, "63": 53}, "uri": "bikecal/linechart.html", "filename": "/home/rbrooks/programs/bike/bikething/templates/bikecal/linechart.html"}
__M_END_METADATA
"""
