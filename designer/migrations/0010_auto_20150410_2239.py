# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def types(apps, schema_editor):
    FieldType = apps.get_model("designer", "FieldType")

    link = FieldType()
    link.name = 'Ссылка'
    link.machine = 'link'
    link.save()


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0009_auto_20150410_2230'),
    ]

    operations = [
        migrations.RunPython(types),
    ]
