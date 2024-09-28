# Standard Library
import sys
import hashlib
from os import path

# Django Core
from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.utils import html, formats, safestring
from django import template as django_template

from django.contrib import messages

# Mako Core
from mako.template import Template as MakoTemplate
from mako.lookup import TemplateLookup
from mako.exceptions import RichTraceback
from webhelpers.html import literal, escape

from mmf_exceptions.renderable import RenderableException

# MMF Core
from mmf.l10n.utils import LocaleHelper, localize_date, localize_number
from mmf.l10n import translation
from mmf.util import json, unescape
from mmf.core.templates import resources
import djangotags

from snippets.pprinting import PrettyDebugger

from mmf.core.templates.mako import helpers
from mmf.social.facebook.authentication import generate_facebook_oauth_url
import mmf.social.helpers as social_helpers
import mmf.route.helpers as maps_helpers

def django_friendly_escape(s):
    #django safestrings can bypass the mako filter...
    uc = unicode(s)
    if isinstance(s, safestring.SafeData) or isinstance(uc, safestring.SafeData):
        return uc
    else:
        return escape(s)


def _get_lookup():
    """
    Returns TemplateLookup Object
    """
    if not hasattr(_get_lookup, 'template_lookup'):
         _get_lookup.template_lookup = TemplateLookup(
            directories=getattr(settings, 'MAKO_TEMPLATE_DIRS', None),
            module_directory=getattr(settings, 'MAKO_MODULE_DIR', None),
            filesystem_checks=getattr(settings, 'DEBUG', False),
            imports=['from mmf.core.templates.mako.template import django_friendly_escape as escape'],
            default_filters=['escape'])
    return _get_lookup.template_lookup


class TemplateBranding(object):
    """
    Helper Object to handle branding...

    """

    def __init__(self, branding):
        self.branding = branding
        self.initialize()

    def initialize(self):
        # Determine Relative Locations...
        self.base = self.branding.base_template + '/base.html'
        self.header = self.branding.base_template + '/header.html'

        # Determine URL...


class TemplateHelper(object):
    """
    Helper/Wrapper Class to Connect to Mako & Do Various Tasks,
    e.g. Fetch Static Resources, i18n (w/ formatting), etc.

    """

    def __init__(self, template, request, context={}, template_is_string=False):
        # Get Template to Render
        if template_is_string:
            self.page_template = MakoTemplate(template, lookup=_get_lookup(),
                module_directory=getattr(settings, 'MAKO_MODULE_DIR', None),
                preprocessor=[],
                imports=['from mmf.core.templates.mako.template import django_friendly_escape as escape'],
                default_filters=['escape'])
        else:
            self.page_template = _get_lookup().get_template(template)

        if request is None:
            raise NotImplementedError('Mako Template Requires User Object, you' +
                                      ' can override this by passing False.')
        elif request is False:
            self._context = {}
        else:
            # Build Resources in Request Object
            if not hasattr(request, 'mmf'):
                try:
                    request.mmf = {}
                except AttributeError:
                    raise TypeError('request is not a WSGIRequest Object, a ' +
                        'common cause may be passing in a tuple/dict containing ' +
                        'the object instead of the object itself. Do you have' +
                        'a decorator that isn\'t properly unpacking args, kwargs?')

            # Set Request, Attributes, and Context Data...
            self.request = request

            try:
                self.branding = self.request.site.branding
            # When I try to import Branding to catch
            # Branding.DoesNotExist, I get an circular import error. So
            # I'll catch ObjectDoesNotExist instead. -Matt McClure,
            # 2013-01-31
            except (AttributeError, ObjectDoesNotExist):
                self.branding = None

            self._context = {
                'branding':self.branding,
                'base_url': '/base/web/base.html',
                'request': self.request,
                'user': self.request.user,
            }

            # Load User...
            if self.request:
                self._context.update({'user':self.request.user, })
            else:
                raise KeyError('Templates require a user object to function.')

            # Django messages framework
            self._context['messages'] = messages.get_messages(self.request)

            self.template_resources = resources.TemplateResources(request, self)

        self._context.update({
            'cache_context': {},
            't': self,
            'j': json.dumps,
            'json': json.dumps,
            'jscript': json.dumphtml,
            'literal': literal,
            'unescape':  unescape.html_entity_decode,
            'l': LocaleHelper(),
            'f': formats,
            'get_format': formats.get_format,
            'localize': formats.localize,
            'localize_date': localize_date,
            'localize_number': localize_number,
            'DEBUG': getattr(settings, 'DEBUG', False),
            'tl': getattr(settings, 'THREADLOCALS', None),
            'pp': PrettyDebugger.prettyprint,
            'login_with_facebook': generate_facebook_oauth_url,
            'social': social_helpers,
            'maps_helpers': maps_helpers,
            'h': helpers
        })

        # Load Django Tags
        if 'django_tags' not in self._context:
            self.context['django_tags'] = {}

        self.context['django_tags'].update(
                django_template.import_library(
                        'django.template.defaulttags').tags)

        self.context.update(
                (key, djangotags._create_mako_filter(value))
                for key, value in
                django_template.import_library(
                        'django.template.defaultfilters').filters.items())

        # Updates the context with the passed-in context, works by side effect
        # of the context property setter.
        self.context = context

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, value): #@DuplicatedSignature
        self._verify_context(value)
        self._context.update(value)

    def set_branding(self, branding):
        # Create TemplateBranding Object
        self.branding = TemplateBranding(branding)
        self.context['base_url'] = self.branding.base

    def _verify_context(self, context):
        for context_key in context:
            if len(context_key) < 3:
                raise NameError('"' + context_key + '" is shorter then 3 chars'\
                    ' and is too short / reserved for context variables.')

    def get_def(self, _def):
        return self.page_template.get_def(_def)

    def render(self, render_func=None):
        """
        Wrapper for Template.render() w/ Proper Exception Handling

        """
        if not render_func:
            render_func = self.page_template.render_unicode

        if hasattr(self, 'request'):
            # Ensure Branding is Provided...
            if type(self.context['branding']) is not TemplateBranding and self.branding:
                self.set_branding(self.branding)

        # Try to Render, Otherwise Return a Mako-Orientated Exception String
        try:
            output = render_func(**self.context)

        # Pass these through to the middleware
        except RenderableException:
            raise

        # This may be an Exceptional Except Exception to Exceptions:
        # Any Exception raised at this point will come from Mako, and
        # since Mako parses template files, the actual errors may appear on
        # lines irrelevant to determining the problem, so we use Mako's
        # Exception rewriter, and capture all Exceptions...
        except Exception:
            # We're mangling the stack frame by doing this stuff, so save it out first
            # olderror[2] is the traceback object
            olderror = sys.exc_info()
            try:
                traceback = RichTraceback()
            except:
                # Sometimes RichTraceback blows up. In that case, just raise the
                # original exception - better than nothing.
                # See http://docs.python.org/reference/simple_stmts.html#raise
                raise olderror[1], None, olderror[2]

            new_exc = MakoTemplateError(traceback.error)

            source = self.page_template.source
            src_hash = hashlib.sha1(source.encode('ascii', 'ignore')).hexdigest()
            bottom_frame = traceback.records[-1]
            # if we are an in memory error, set the culprit explicitly (for sentry agg)
            if bottom_frame[0].startswith('memory'):
                culprit = "Mako in memory %s:%s" % (src_hash, bottom_frame[1])
                new_exc.culprit = culprit

            # record the hash of the source for later stack rewriting
            new_exc.extra = {'source_hash': src_hash}

            # get all the information sentry needs to display the template interface.
            # sometimes templates call back into python code and that code throws the
            # exception, so we walk the stack until we find the template frame
            template_frame = None
            for frame in reversed(traceback.records):
                if frame[5] is not None:
                    template_frame = frame
                    break
            if template_frame:
                lineno = template_frame[5] - 1
                if template_frame[0].startswith('memory'):
                    filename = src_hash
                    abs_path = 'memory'
                else:
                    filename = path.basename(template_frame[0])
                    abs_path = path.dirname(template_frame[0])
                src_lines = source.split('\n')
                if len(src_lines) > lineno:
                    context_line = src_lines[lineno]
                else:
                    context_line = ''
                new_exc.template = {
                    'filename': filename,
                    'abs_path': abs_path,
                    'pre_context': src_lines[:lineno][-2:],
                    'context_line': context_line,
                    'lineno': lineno,
                    'post_context': src_lines[lineno + 1:][:2],
                }

            raise new_exc, None, olderror[2]

        return unicode(output)

    def render_def(self, name):
        """
        Wrapper for get_def.render w / Proper Exception Handling
        """
        return self.render(self.page_template.get_def(name).render_unicode)

    #These are to make translation methods available from inside mako templates.
    #They should *not* be called from ordinary python code.
    def _(self, str_text, *args, **kwargs):
        return translation._(str_text, *args, **kwargs)
    def ugettext(self, str_text, *args, **kwargs):
        return translation.ugettext(str_text).format(**kwargs)
    def ugettext_noop(self, str_text, *args, **kwargs):
        return translation.ugettext_noop(str_text).format(**kwargs)

    def generate_module(self, module, cls_name, cache_context, render_context=None, *args, **kwargs):
        mod = __import__(''.join(['modules.', module]), globals(), locals(), fromlist=[cls_name])
        cls = getattr(mod, cls_name)

        templatemodule = cls(cache_context=cache_context, *args, **kwargs)
        return templatemodule.generate(**render_context)

    def url(self, viewname, urlconf=None, current_app=None, *args, **kwargs):
        """
        update to url function to allow easier use in mako ${} constructs
        (kwargs are directly passed through).
        CAVEAT: if your url expects named arguments named 'urlconf' or
        'current_app' or possibly 'viewname', they will be caught by the
        'arguments to reverse' parsing instead; in that case you must use
        url('viewname', kwargs=dict(urlconf='foobar', viewname='bazfizz'))
        """
        #viewname, urlconf=None, args=None, kwargs=None, current_app=None
        kwargs.update(kwargs.pop('kwargs', {}))
        args += tuple(kwargs.pop('args', []))

        return urlresolvers.reverse(viewname, urlconf=urlconf, current_app=current_app,
            args=args, kwargs=kwargs)

    def debug(self, var, style=False):
        """
        TODO Implement some AJAX
        """

        if var == 'context':
            var = self.context

        object_type = str(type(var)).replace('type', '').strip('<>\' ')

        result = '<b>' + object_type + '</b>\n'

        if type(var) is dict:

            try:
                for k, v in var.items():
                    key_type = str(type(k)).replace('type', '').strip('<>\' ')
                    key = str(k)
                    value_type = str(type(v)).replace('type', '').strip('<>\' ')
                    value = html.escape(str(v))

                    result += '(' + key_type + ')' + key + ' : ' + '(' + value_type + ')' + value + '\n'
            except Exception as e:
                result += '<b style="color:red">Error</b>: Exception raised ' + \
                'when attempting to get the value of (' + key_type + ')' + key + \
                '\n<i>' + str(e) + '</i> '

        else:
            result += '\n__str__: \n' + unicode(var).strip('<>\' ') if var else ''
            try:
                result += '\n\n__dict__: \n'

                if type(var.__dict__) is dict:
                    for k, v in var.__dict__.items():
                        key_type = str(type(k)).replace('type', '').strip('<>\' ')
                        key = str(k)
                        value_type = str(type(v)).replace('type', '').strip('<>\' ')
                        value = html.escape(str(v))

                        result += '(' + key_type + ')' + key + ' : ' + '(' + value_type + ')' + value + '\n'
            except:
                pass

        return result

    def get_setting(self, setting):
        """Get a setting from templatehelper scope (template function)"""
        return getattr(settings, setting, None)

class MakoTemplateError(Exception):
    pass
