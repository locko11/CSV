from django.forms import ModelForm, IntegerField
from .models import Schema, Columns


class SchemaForm(ModelForm):
    class Meta:
        model = Schema
        fields = ['schame_name', 'column_separator', 'string_character', 'user']


class ColumnForm(ModelForm):
    class Meta:
        model = Columns
        fields = ['name', 'type', 'order', 'schema']


class ColumnEditForm(ModelForm):

    id = IntegerField(required=False)

    class Meta:
        model = Columns
        fields = ['name', 'type', 'order', 'schema', 'id']


