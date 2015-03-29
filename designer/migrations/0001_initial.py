# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import designer.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('right', models.IntegerField(default=0)),
                ('left', models.IntegerField(default=0)),
                ('date_create', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('date_modify', models.DateTimeField(verbose_name='Посл. изменения', auto_now_add=True)),
                ('name', models.CharField(verbose_name='Название', max_length=255)),
                ('layer', models.IntegerField(default=1000, verbose_name='Номер слоя')),
                ('default', models.BooleanField(default=False, verbose_name='Отображать по умолчанию', help_text='Отображать по умолчанию если не выбрано другое')),
                ('display', models.BooleanField(default=True, verbose_name='Опубликовано', help_text='Отображать на сайте или нет')),
                ('root', models.ForeignKey(null=True, blank=True, help_text='Three of steps', to='designer.Catalog')),
            ],
            options={
                'verbose_name_plural': 'элементы',
                'verbose_name': 'элемент',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=255)),
                ('machine', models.CharField(unique=True, verbose_name='Машинное имя', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('number', models.IntegerField(default=1, help_text='Номер положения', verbose_name='Номер')),
                ('file', models.ImageField(upload_to=designer.models.Helper.catalog_main_image, verbose_name='Изображение')),
                ('parent', models.ForeignKey(to='designer.Catalog')),
            ],
            options={
                'verbose_name_plural': 'изображения',
                'verbose_name': 'изображение',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='catalog',
            name='type',
            field=models.ForeignKey(help_text='Тип поля для отображения', to='designer.FieldType', verbose_name='Тип поля'),
            preserve_default=True,
        ),
    ]
