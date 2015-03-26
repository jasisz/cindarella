# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'stories'},
        ),
        migrations.AddField(
            model_name='story',
            name='max_mutations',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='min_mutations',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='variant',
            name='template',
            field=models.TextField(default='template'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variant',
            name='hash',
            field=models.CharField(primary_key=True, serialize=False, editable=False, max_length=350),
        ),
        migrations.AlterField(
            model_name='variant',
            name='options_dict',
            field=jsonfield.fields.JSONField(default='{}'),
        ),
    ]
