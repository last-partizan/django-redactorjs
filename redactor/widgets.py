import json

from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings


GLOBAL_OPTIONS = getattr(settings, 'REDACTOR_OPTIONS', {})
JQUERY_URL = getattr(settings, 'JQUERY_URL', None)

INIT_JS = """<script type="text/javascript">
    var $ = window.jQuery || (window.django || {}).jQuery;
    if ($) { (function($){ $("#%(id)s").redactor(%(opts)s); })($); }
    else {
        if (!window._redactor_options) window._redactor_options = {};
        window._redactor_options["#%(id)s"] = %(opts)s;
    }
    </script>
    """

redactor_js = [
    'redactor/redactor%s.js' % ("" if settings.DEBUG else ".min"),
    'redactor/init.js',
]

if JQUERY_URL:
    redactor_js.insert(0, JQUERY_URL)


class RedactorEditor(widgets.Textarea):

    class Media:
        js = redactor_js

        css = {
            'all': (
                'redactor/css/redactor.css',
                'redactor/css/django_admin.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('redactor_options', {})
        super(RedactorEditor, self).__init__(*args, **kwargs)
        self.add_language_file()

    def get_options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        options.update({
            'imageUpload': reverse('redactor_upload_image', kwargs={'upload_to': self.upload_to}),
            'fileUpload': reverse('redactor_upload_file', kwargs={'upload_to': self.upload_to})
        })
        return json.dumps(options)

    def add_language_file(self):
        lang = self.custom_options.get(
                'lang', GLOBAL_OPTIONS.get('lang', None))
        if lang:
            self.Media.js.insert(0, 'redactor/langs/%s.js' % lang)

    def render(self, name, value, attrs=None):
        html = super(RedactorEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        html += INIT_JS % {'id': id_, 'opts': self.get_options()}
        return mark_safe(html)


# For backward compatibility
JQueryEditor = RedactorEditor
