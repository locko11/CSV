from django.forms import ModelForm, IntegerField, ModelChoiceField
from .models import Schema, Columns
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.contrib.auth.models import User

class SchemaForm(ModelForm):
    id = IntegerField(required=False)
    class Meta:
        model = Schema
        fields = ['schame_name', 'column_separator', 'string_character', 'user', 'id']
        labels = {
            'schame_name': ('Schame name'),
            'column_separator': ('Column separator'),
            'string_character': ('String character'),

        }


class ColumnForm(ModelForm):
    class Meta:
        model = Columns
        fields = ['name', 'type', 'order', 'schema']


class ColumnEditForm(ModelForm):

    id = IntegerField(required=False)

    class Meta:
        model = Columns
        fields = ['name', 'type', 'order', 'schema', 'id']


SchemaFormset = inlineformset_factory(Schema, Columns, fields=('name', 'type', 'order'), extra=0)


