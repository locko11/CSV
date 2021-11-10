from django.contrib import admin
from .models import Schema, Columns, CSV_Files


admin.site.register(Schema)
admin.site.register(Columns)
admin.site.register(CSV_Files)
# Register your models here.
