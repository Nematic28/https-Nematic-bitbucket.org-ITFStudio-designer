# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0011_auto_20150501_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldtype',
            name='autoload',
            field=models.BooleanField(default=False, verbose_name='Авто подгрузка данынх'),
        ),
        migrations.AddField(
            model_name='fieldtype',
            name='storage',
            field=models.CharField(max_length=255, default='outer', verbose_name='Тип хранения данных', choices=[('inner', 'Внутри'), ('outer', 'Снаружи')]),
        ),
    ]
