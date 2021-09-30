from django.contrib.auth.models import User
from django.db import models


class Schema(models.Model):
    SEPARATORS = (
        ('comma', 'Comma (,)'),
    )
    STRINGS_CHARAKTERS = (
        ('duble-quote', 'Double-quote (“)'),
    )
    schame_name = models.CharField(max_length=250, unique=True)
    column_separator = models.CharField(max_length=20, choices=SEPARATORS, default='comma')
    string_character = models.CharField(max_length=20, choices=STRINGS_CHARAKTERS, default='duble-quote')
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='schemas', on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ['user', 'schame_name']
        ordering = ['updated']

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
    schema = models.ForeignKey(Schema, related_name='column', on_delete=models.CASCADE)

    class Meta:
        unique_together = [['schema', 'order'], ['schema', 'name']]
        ordering = ['order']

    def __str__(self):
        return self.name




