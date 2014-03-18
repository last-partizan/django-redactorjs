#-*- coding: utf-8 -*-
from django.db.models import Field
from redactor.widgets import RedactorEditor


class RedactorField(Field):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop('redactor_options', {})
        upload_to = kwargs.pop('upload_to', '')
        self.widget = RedactorEditor(redactor_options=options, upload_to=upload_to)
        super(RedactorField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        defaults = {'widget': self.widget}
        defaults.update(kwargs)
        return super(RedactorField, self).formfield(**defaults)
      
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^redactor\.fields\.RedactorField'])
except ImportError:
    pass
