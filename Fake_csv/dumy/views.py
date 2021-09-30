from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Schema, Columns
from .forms import SchemaForm, ColumnForm
from django.views.generic import ListView
from .tasks import mul


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
    if request.POST:
        schema = {"schame_name":request.POST.get("schema_name"), \
                                       "column_separator":request.POST.get("column_separator"),\
                                       "string_character":request.POST.get("string_character"),\
                                       "user":request.user}
        schema_form = SchemaForm(schema)
        if schema_form.is_valid():
            schema_obj = schema_form.save()
            print(f'ok {schema_obj}')
        else:

            return render(request,
                      'account/new_schema.html', {'schema_form': schema_form})

        rows = all_rows(request.POST)
        columns = rows_contain(rows, schema_obj)
        for column in columns.values():
            col_form = ColumnForm(column)
            if col_form.is_valid():
                col_form.save()
            else:
                return render(request,
                              'account/new_schema.html', {'col_form': col_form})
        return render(request, 'account/dashboard.html')
    return render(request, 'account/new_schema.html')



def edit_schema(request, username, schema_id):
    schema = Schema.objects.get(id=schema_id)
    clumns = Columns.objects.filter(schema_id=schema_id)
    if request.POST:

        schema_data = {"schame_name": request.POST.get("schema_name"), \
                  "column_separator": request.POST.get("column_separator"), \
                  "string_character": request.POST.get("string_character"), \
                  "user": request.user
                  }
        schema_form = SchemaForm(schema_data, instance=schema)

        if schema_form.is_valid():
            col_form = update_columns(request, schema)
            if col_form.errors:
                print(col_form.errors.items())


                return render(request, 'account/edit_schema.html',
                              {"schema": schema, "clumns": clumns, "col_form": col_form})
            schema_form.save()
            return redirect('dashboard')
        else:
            return render(request, 'account/edit_schema.html',
                          {"schema": schema, "clumns": clumns, "schema_errors": schema_form})

    return render(request, 'account/edit_schema.html', {"schema": schema, "clumns": clumns})


def schema_sets(request, username, schema_id):
    r = mul.delay(5)
    if r.ready():
        return HttpResponse(r.get())
    return HttpResponse('by')
