from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField


class Schema(models.Model):
    SEPARATORS = (
        ('comma', 'Comma (,)'),
        ('sіemicolon', 'Semicolon (;)'),
    )
    STRINGS_CHARAKTERS = (
        ('duble-quote', 'Double-quote (“)'),
    )
    id = models.AutoField(primary_key=True, blank=True)
    schame_name = models.CharField(max_length=100)
    column_separator = models.CharField(max_length=20, choices=SEPARATORS, default='comma')
    string_character = models.CharField(max_length=20, choices=STRINGS_CHARAKTERS, default='duble-quote')
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='schemas', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['user', 'schame_name']
        ordering = ['-updated']

    def __str__(self):
        return self.schame_name


class Columns(models.Model):
    TYPES = (
        ('full_name', 'Full name'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('company_name', 'Company name'),
        ('phone_number', 'Phone number'),

    )
    id = models.AutoField(primary_key=True, blank=True)
    name = models.CharField(max_length=50, blank=False)
    type = models.CharField(max_length=50, choices=TYPES, default='email', blank=False)
    order = models.IntegerField(blank=False)
    schema = models.ForeignKey(Schema, related_name='columns', on_delete=models.CASCADE)

    class Meta:
        # unique_together = [['schema', 'order'], ['schema', 'name']]
        unique_together = (('schema', 'order'), ('schema', 'name'))
        ordering = ['order']

    def __str__(self):
        return self.name



def tool(insance):
    print(insance)
    print(insance.id)
    return f"{insance.schema.user}-{insance.schema.schame_name}-{insance.create}",

class CSV_Files(models.Model):
    schema = models.ForeignKey(Schema, related_name='files', on_delete=models.CASCADE)
    # file_name = models.SlugField(max_length=255, unique=True, blank=True)
    create = models.DateTimeField(auto_now=True)
    file_name = AutoSlugField(populate_from=tool,
                         unique_with=['schema__schame_name', 'schema__user','create'])

    class Meta:
        # unique_together = [['schema', 'order'], ['schema', 'name']]
        ordering = ['pk']

    def __str__(self):
        return self.file_name

    def save(self, *args, **kwargs):


        # value = f'{self.schema.user}-{self.schema.schame_name}-{self.create}'
        # print(file)
        # self.file_name = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
