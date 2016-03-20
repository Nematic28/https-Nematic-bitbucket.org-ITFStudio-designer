# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import designer.models


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0011_auto_20150501_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selector',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=255)),
                ('icon', models.ImageField(blank=True, verbose_name='Иконка', upload_to=designer.models.Helper.dop_image)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=255)),
                ('icon', models.ImageField(blank=True, verbose_name='Иконка', upload_to=designer.models.Helper.dop_image)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Texture',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='catalog',
            name='selector',
            field=models.ForeignKey(help_text='Иконка переключателя', to='designer.Selector', verbose_name='Иконка переключателя',null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalog',
            name='color',
            field=models.ForeignKey(help_text='Цвет', to='designer.Color', verbose_name='Цвет',null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='catalog',
            name='texture',
            field=models.ForeignKey(help_text='Текстура', to='designer.Texture', verbose_name='Текстура',null=True, blank=True),

        ),
    ]

