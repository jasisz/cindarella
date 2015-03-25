# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField(null=True, blank=True)),
                ('attribute', models.ForeignKey(to='stories.Attribute', related_name='options')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('template', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('hash', models.CharField(primary_key=True, serialize=False, max_length=350)),
                ('options_dict', jsonfield.fields.JSONField()),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('options', models.ManyToManyField(to='stories.Option', related_name='variants')),
                ('parent', mptt.fields.TreeForeignKey(null=True, blank=True, to='stories.Variant', related_name='children')),
                ('story', models.ForeignKey(to='stories.Story')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='attribute',
            name='story',
            field=models.ForeignKey(to='stories.Story', related_name='attributes'),
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set([('name', 'story')]),
        ),
    ]
