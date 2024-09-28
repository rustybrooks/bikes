# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1474419404.039681
_enable_loop = True
_template_filename = '/home/rbrooks/programs/bike/bikething/templates/bikecal/segment.html'
_template_uri = 'bikecal/segment.html'
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
        def header():
            return render_header(context._locals(__M_locals))
        efforts = context.get('efforts', UNDEFINED)
        len = context.get('len', UNDEFINED)
        history = context.get('history', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\r\n\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        __M_writer(u'\r\n\r\n<p>\r\n<b>Rank History</b>\r\n\r\n<table border="1" cellspacing="0">\r\n    <tr>\r\n        <th>Date</th>\r\n        <th>Rank</th>\r\n        <th>Entries</th>\r\n        <th>Avg HR</th>\r\n        <th>Avg PWR</th>\r\n        <th>Distance</th>\r\n        <th>Elapsed</th>\r\n        <th>Moving</th>\r\n    </tr>\r\n\r\n')
        for h in history:
            __M_writer(u'    <tr>\r\n        <td>')
            __M_writer(unicode(h.recorded_datetime.strftime("%Y-%m-%d")))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.rank))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.entries))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.average_hr))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.average_watts))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.distance))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.elapsed_time))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(h.moving_time))
            __M_writer(u'</td>\r\n    </tr>\r\n')
        __M_writer(u'\r\n</table>\r\n\r\n\r\n<p>\r\n<b>Effort History (')
        __M_writer(unicode(len(efforts)))
        __M_writer(u')</b>\r\n<table border="1" cellspacing="0">\r\n    <tr>\r\n        <th>Date</th>\r\n        <th>Elapsed</th>\r\n        <th>Moving</th>\r\n        <th>Cadence</th>\r\n        <th>HR</th>\r\n        <th>PWR</th>\r\n        <th>Rank</th>\r\n        <th>PR Rank</th>\r\n    </tr>\r\n\r\n')
        for e in efforts:
            __M_writer(u'    <tr>\r\n        <td>')
            __M_writer(unicode(e.start_datetime_local.strftime("%Y-%m-%d")))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(e.elapsed_time))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(e.moving_time))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(e.average_cadence))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(e.average_heartrate))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode('*' if e.device_watts else ''))
            __M_writer(unicode(e.average_watts))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(e.kom_rank if e.kom_rank else ''))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(e.pr_rank if e.pr_rank else ''))
            __M_writer(u'</td>\r\n    </tr>\r\n')
        __M_writer(u'</table>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def header():
            return render_header(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"27": 0, "37": 1, "42": 3, "43": 20, "44": 21, "45": 22, "46": 22, "47": 23, "48": 23, "49": 24, "50": 24, "51": 25, "52": 25, "53": 26, "54": 26, "55": 27, "56": 27, "57": 28, "58": 28, "59": 29, "60": 29, "61": 32, "62": 37, "63": 37, "64": 50, "65": 51, "66": 52, "67": 52, "68": 53, "69": 53, "70": 54, "71": 54, "72": 55, "73": 55, "74": 56, "75": 56, "76": 57, "77": 57, "78": 57, "79": 58, "80": 58, "81": 59, "82": 59, "83": 62, "89": 3, "100": 89}, "uri": "bikecal/segment.html", "filename": "/home/rbrooks/programs/bike/bikething/templates/bikecal/segment.html"}
__M_END_METADATA
"""
