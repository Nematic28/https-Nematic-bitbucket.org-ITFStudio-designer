# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='type',
            field=models.ForeignKey(to='designer.FieldType', verbose_name='Тип под элементов', help_text='Тип под элемента для отображения'),
            preserve_default=True,
        ),
    ]
