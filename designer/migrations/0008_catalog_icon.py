# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import designer.models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0005_auto_20150329_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalog',
            name='icon',
            field=models.ImageField(blank=True, verbose_name='Иконка', upload_to=designer.models.Helper.catalog_logo),
            preserve_default=True,
        ),
    ]
