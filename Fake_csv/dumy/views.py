from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Schema, Columns
from .forms import SchemaForm, ColumnForm
from django.views.generic import ListView
from .tasks import mul
from django.forms import BaseInlineFormSet, inlineformset_factory


def all_rows(dict):
    row_dict = {}
    for word in dict.keys():
        if 'row' in word:
            row_dict.update({word: dict.get(word)})
    return row_dict


def rows_contain(dict, schema):
    d = {}
    for f in dict.keys():
        name, row = f.split('_')
        if d.get(row):
            d.get(row).update({name: dict.get(f)})
        else:
            d.update({row: {name: dict.get(f), "schema": schema}})
    return d

def col_id_to_del(current_columns, previous_columns):
    return [id for id in previous_columns if id not in current_columns]


def create_col(columns):
    for column in columns.values():
        if 'id' in column.keys():
            inst = Columns.objects.get(id=column.get('id'))
            col_form = ColumnForm(column, instance=inst)
        else:
            col_form = ColumnForm(column)
        if col_form.is_valid():
            col_form.save()
        else:
            return col_form

def update_columns(request, schema_obj):
    rows = all_rows(request.POST)
    columns = rows_contain(rows, schema_obj)
    print(columns.values())
    # print(f'col   { [d.get("id") for d in columns.values()]}')

    previous_columns_id = [id.get('id') for id in Columns.objects.filter(schema_id=schema_obj.id).values('id')]

    print(f'previous_columns_id = {previous_columns_id}')

    cur_id = [int(d.get("id")) for d in columns.values() if "id" in d.keys()]
    print(f'cur_id = {cur_id}')
    ids_to_del = col_id_to_del(cur_id, previous_columns_id)

    # map(lambda id: Columns.objects.get(id=id).delete(), ids_to_del)
    [Columns.objects.get(id=id).delete() for id in ids_to_del]
    col_form = create_col(columns)
    print('ok')
    if col_form:
        return col_form
    # [Columns.objects.get(id=id).delete() for id in ids_to_del]



@login_required
def dashboard(request):
    list = Schema.objects.filter(user=request.user)
    return render(request, 'account/dashboard.html', {'schemas_list': list})



def hendler(request):
    print(dir(request.POST))
    return HttpResponse(dir(request.POST))




def new_schema(request):
    SchemaFormset = inlineformset_factory(Schema, Columns, fields=('name', 'type', 'order'), extra=0)

    col_formset = SchemaFormset()
    sch_form = SchemaForm()


    if request.method == 'POST':
        sch_form = SchemaForm(request.POST)

        if sch_form.is_valid():
            schema = sch_form.save()

        else:
            # return render(request, 'account/schema.html', {"sch_form": sch_form, "col_formset": col_formset})
            return render(request, 'account/schema.html', {"sch_form": sch_form, "col_formset": col_formset})
        col_formset = SchemaFormset(request.POST)
        print(request.POST)
        if col_formset.is_valid():

            for col_form in [i for i in col_formset if i not in col_formset.deleted_forms]:
                    print(col_form.cleaned_data)
                    col = col_form.save(commit=False)
                    col.schema = schema
                    col.save()
            return redirect('/')
        else:
            print(col_formset.errors)
            schema.delete()
            return render(request, 'account/schema.html', {"sch_form": sch_form, "col_formset": col_formset})
    return render(request, 'account/schema.html', {"sch_form": sch_form, "col_formset": col_formset})

    # {'csrfmiddlewaretoken': 'ukfIBF4bVigpL7uM7PwQxm3quXRcb1LkrXb4sRdnOztJQmUlucnbJNri0GLZovAu',
    #  'schame_name': 'ADSAF223', 'column_separator': 'comma', 'string_character': 'duble-quote', 'id': '',
    #  'user': '1', 'column-0-id': '', 'column-0-name': 'asdfewarf', 'column-0-type': 'email',
    #  'column-0-order': '2', 'column-1-id': '', 'column-1-name': 'azdfv',
    #  'column-1-type':'email', 'column-1-order': '2', 'column-1-DELETE': 'on',
    #  'column-2-id': '',
    #  'column-2-name': 'sadfsdf', 'column-2-type': 'email', 'column-2-order': '1', 'column-TOTAL_FORMS': '3',
    #  'column-INITIAL_FORMS': '0', 'column-MIN_NUM_FORMS': '0', 'column-MAX_NUM_FORMS': '1000'}
    # {'name': 'SAFDSF', 'type': 'email', 'order': 1, 'id': None, 'DELETE': False, 'schema': < Schema: >}
    # {'name': 'SDFSD', 'type': 'email', 'order': 2, 'id': None, 'DELETE': False, 'schema': < Schema: >}
    # {'name': 'SDGSD1', 'type': 'email', 'order': 2, 'id': None, 'DELETE': True, 'schema': < Schema: >}
    # if request.POST:
    #     schema = {"schame_name":request.POST.get("schema_name"), \
    #                                    "column_separator":request.POST.get("column_separator"),\
    #                                    "string_character":request.POST.get("string_character"),\
    #                                    "user":request.user}
    #     schema_form = SchemaForm(schema)
    #     if schema_form.is_valid():
    #         schema_obj = schema_form.save()
    #         print(f'ok {schema_obj}')
    #     else:
    #
    #         return render(request,
    #                   'account/new_schema.html', {'schema_form': schema_form})
    #
    #     rows = all_rows(request.POST)
    #     columns = rows_contain(rows, schema_obj)
    #     for column in columns.values():
    #         col_form = ColumnForm(column)
    #         if col_form.is_valid():
    #             col_form.save()
    #         else:
    #             return render(request,
    #                           'account/new_schema.html', {'col_form': col_form})
    #     return render(request, 'account/dashboard.html')





def edit_schema(request, username, schema_id):
    SchemaFormset = inlineformset_factory(Schema, Columns, fields=('name', 'type', 'order'), extra=0)
    schema = get_object_or_404(Schema, pk=schema_id)
    col_formset = SchemaFormset(instance=schema)
    sch_form = SchemaForm(instance=schema)
    if request.method == 'POST':
        sch_form = SchemaForm(request.POST, instance=schema)
        col_formset = SchemaFormset(request.POST, instance=schema)
        if sch_form.is_valid() and col_formset.is_valid():
            schema = sch_form.save()
            for frm in col_formset.deleted_forms:
                print(dir(col_formset))
                print(col_formset.can_delete)
            for col_form in col_formset :
                if col_formset.can_delete:
                    col = col_form.save(commit=False)
                    col.schema = schema
                    col.save()
            return redirect('/')

        else:
            # return render(request, 'account/schema.html', {"sch_form": sch_form, "col_formset": col_formset})
            return render(request, 'account/edit_schema.html', {"sch_form": sch_form, "col_formset": col_formset})



    return render(request, 'account/edit_schema.html', {"sch_form": sch_form, "col_formset": col_formset})
    # schema = Schema.objects.get(id=schema_id)
    # clumns = Columns.objects.filter(schema_id=schema_id)
    #
    # if request.POST:
    #
    #     schema_data = {"schame_name": request.POST.get("schema_name"), \
    #               "column_separator": request.POST.get("column_separator"), \
    #               "string_character": request.POST.get("string_character"), \
    #               "user": request.user
    #               }
    #     schema_form = SchemaForm(schema_data, instance=schema)
    #
    #     if schema_form.is_valid():
    #         col_form = update_columns(request, schema)
    #         if col_form.errors:
    #             print(col_form.errors.items())
    #
    #             return render(request, 'account/edit_schema.html',
    #                           {"schema": schema, "clumns": clumns, "col_form": col_form})
    #         schema_form.save()
    #         return redirect('dashboard')
    #     else:
    #         return render(request, 'account/edit_schema.html',
    #                       {"schema": schema, "clumns": clumns, "schema_errors": schema_form})
    #
    # return render(request, 'account/edit_schema.html', {"schema": schema, "clumns": clumns})


def schema_sets(request, username=None, schema_id=None):
    # if schema_id or username:
    #     SchemaFormset = inlineformset_factory(Schema, Columns, fields=('name', 'type', 'order'), extra=0)
    #     schema = Schema.objects.get(id=schema_id)
    #     formset = SchemaFormset(instance=schema)
    #     sh_form = SchemaForm(instance=schema)
    #     print(formset)
    #     if request.POST:
    #         print(dir(request.POST))
    #         d= SchemaForm(request.POST)
    #
    #         f = SchemaFormset(request.POST)
    #         for i in f:
    #             if i.is_valid():
    #                 print(i.cleaned_data)
    #             print(i.cleaned_data)
    #     return render(request, 'account/test.html', {"formset": formset, "sh_form": sh_form, "schema": schema})
    print(schema_id, username)
    if request.method == 'GET':
        schema_files = Schema.objects.get(id=schema_id).files.all()
        return render(request, 'account/test.html', {"schema_files": schema_files})



# def new_schema(request):
#     if request.POST:
#         schema = {"schame_name":request.POST.get("schema_name"), \
#                                        "column_separator":request.POST.get("column_separator"),\
#                                        "string_character":request.POST.get("string_character"),\
#                                        "user":request.user}
#         schema_form = SchemaForm(schema)
#         if schema_form.is_valid():
#             schema_obj = schema_form.save()
#             print(f'ok {schema_obj}')
#         else:
#
#             return render(request,
#                       'account/new_schema.html', {'schema_form': schema_form})
#
#         rows = all_rows(request.POST)
#         columns = rows_contain(rows, schema_obj)
#         for column in columns.values():
#             col_form = ColumnForm(column)
#             if col_form.is_valid():
#                 col_form.save()
#             else:
#                 return render(request,
#                               'account/new_schema.html', {'col_form': col_form})
#         return render(request, 'account/dashboard.html')
#     return render(request, 'account/schema.html')

