# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0012_auto_20150512_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtype',
            name='machine',
            field=models.CharField(choices=[('radio', 'Переключатель'), ('label', 'Заголовок'), ('link', 'Ссылка'), ('step', 'Шаг'), ('popup', 'Всплывающее окно')], verbose_name='Машинное имя', max_length=255, unique=True),
        ),
    ]
