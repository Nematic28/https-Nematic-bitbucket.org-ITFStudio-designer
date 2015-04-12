# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0008_catalog_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fieldtype',
            options={'verbose_name': 'тип', 'verbose_name_plural': 'типы'},
        ),
    ]
