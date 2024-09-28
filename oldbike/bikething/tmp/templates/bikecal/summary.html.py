# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1474476378.612123
_enable_loop = True
_template_filename = '/home/rbrooks/programs/bike/bikething/templates/bikecal/summary.html'
_template_uri = 'bikecal/summary.html'
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
        workouts = context.get('workouts', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\r\n\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        __M_writer(u'\r\n\r\n')

        week = workouts[0].start_datetime_local.strftime("%W")
        summary = {
            'elev': 0, 'dist': 0, 'time': 0, 'kj': 0, 'kj_time': 0, 'cheevos': 0,
        }
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['week','summary'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\r\n\r\n<table border="1" cellpadding="2" cellspacing="0">\r\n    <tr>\r\n        <th>Date</th>\r\n        <th>Day</th>\r\n        <th>Elapsed</th>\r\n        <th>Moving</th>\r\n        <th>Distance</th>\r\n        <th>Avg Spd</th>\r\n        <th>Avg PWR</th>\r\n        <th>KJ</th>\r\n        <th>Elev Gain</th>\r\n        <th>Elev/Mi</th>\r\n        <th>Avg HR</th>\r\n        <th>Suffer</th>\r\n        <th>Cheevos</th>\r\n    </tr>\r\n\r\n')
        for wo in workouts:
            __M_writer(u'\r\n\r\n')
            if wo.start_datetime_local.strftime("%W") != week:
                __M_writer(u'    <tr>\r\n        <td colspan="3">Weekly Summary</td>\r\n        <td align="right">')
                __M_writer(unicode(wo.time_formatted(summary['time'])))
                __M_writer(u'</td>\r\n        <td align="right">')
                __M_writer(unicode("%0.1f" % summary['dist']))
                __M_writer(u'</td>\r\n        <td align="right">')
                __M_writer(unicode("%0.1f" % (summary['dist'] / (summary['time']/3600.),)))
                __M_writer(u'</td>\r\n        <td align="right">')
                __M_writer(unicode("%0.0f" % (1000*summary['kj']/summary['kj_time'])))
                __M_writer(u'</td>\r\n        <td align="right">')
                __M_writer(unicode("%0.0f" % summary['kj']))
                __M_writer(u'</td>\r\n        <td align="right">')
                __M_writer(unicode("%0.0f" % summary['elev']))
                __M_writer(u'</td>\r\n        <td align="right">')
                __M_writer(unicode("%0.0f" % (summary['elev']/summary['dist'] if summary['dist'] else 0)))
                __M_writer(u'</td>\r\n        <td colspan="2">&nbsp</td>\r\n        <td align="right">')
                __M_writer(unicode(summary['cheevos']))
                __M_writer(u'</td>\r\n    </tr>\r\n\r\n    <tr><td colspan="13">&nbsp;</td></tr>\r\n    ')

                week = wo.start_datetime_local.strftime("%W")
                summary = {
                    'elev': 0, 'dist': 0, 'time': 0, 'kj': 0, 'kj_time': 0,  'cheevos': 0
                    }
                    
                
                __M_locals_builtin_stored = __M_locals_builtin()
                __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['week','summary'] if __M_key in __M_locals_builtin_stored]))
                __M_writer(u'\r\n')
            __M_writer(u'\r\n    ')

            summary['dist'] += wo.distance_miles()
            summary['time'] += wo.moving_time
            summary['elev'] += wo.total_elevation_gain_feet()
            summary['kj'] += wo.kilojoules or 0
            summary['kj_time'] += wo.moving_time if wo.kilojoules else 0
            summary['cheevos'] += wo.achievement_count or 0
                
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\r\n\r\n    <tr>\r\n        <td>')
            __M_writer(unicode(wo.start_datetime_local.strftime('%Y-%m-%d %H:%M')))
            __M_writer(u'</td>\r\n        <td>')
            __M_writer(unicode(wo.start_datetime_local.strftime('%a')))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode(wo.elapsed_time_formatted()))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode(wo.moving_time_formatted()))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode("%0.1f" % wo.distance_miles()))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode("%0.1f" % wo.average_speed_miles()))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode("%0.0f" % wo.average_watts if wo.average_watts else ""))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode("%0.0f" % (wo.kilojoules or 0)))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode("%0.0f" % wo.total_elevation_gain_feet()))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode("%0.0f" % (wo.total_elevation_gain_feet() / wo.distance_miles() if wo.distance_miles() else 0, )))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode(("%0.0f" % wo.average_heartrate) if wo.average_heartrate else ''))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode(wo.suffer_score or ''))
            __M_writer(u'</td>\r\n        <td align="right">')
            __M_writer(unicode(wo.achievement_count))
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
{"source_encoding": "ascii", "line_map": {"137": 126, "27": 0, "35": 1, "40": 3, "41": 5, "50": 10, "51": 29, "52": 30, "53": 32, "54": 33, "55": 35, "56": 35, "57": 36, "58": 36, "59": 37, "60": 37, "61": 38, "62": 38, "63": 39, "64": 39, "65": 40, "66": 40, "67": 41, "68": 41, "69": 43, "70": 43, "71": 47, "80": 52, "81": 54, "82": 55, "93": 62, "94": 65, "95": 65, "96": 66, "97": 66, "98": 67, "99": 67, "100": 68, "101": 68, "102": 69, "103": 69, "104": 70, "105": 70, "106": 71, "107": 71, "108": 72, "109": 72, "110": 73, "111": 73, "112": 74, "113": 74, "114": 75, "115": 75, "116": 76, "117": 76, "118": 77, "119": 77, "120": 80, "126": 3}, "uri": "bikecal/summary.html", "filename": "/home/rbrooks/programs/bike/bikething/templates/bikecal/summary.html"}
__M_END_METADATA
"""
