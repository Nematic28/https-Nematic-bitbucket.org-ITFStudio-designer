# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0002_auto_20150304_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='type',
            field=models.ForeignKey(help_text='Тип элемента для отображения', verbose_name='Тип элемента', to='designer.FieldType'),
            preserve_default=True,
        ),
    ]
