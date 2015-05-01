# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def types(apps, schema_editor):
    FieldType = apps.get_model("designer", "FieldType")
    step = FieldType()
    step.name = 'Шаг'
    step.machine = 'step'
    step.save()


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0010_auto_20150410_2239'),
    ]

    operations = [
        migrations.RunPython(types),
    ]
