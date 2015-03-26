# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_auto_20150325_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='text',
        ),
        migrations.AddField(
            model_name='option',
            name='body',
            field=jsonfield.fields.JSONField(null=True, blank=True, default='{}'),
        ),
    ]
