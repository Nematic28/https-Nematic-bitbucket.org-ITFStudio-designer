# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_popup(apps, schema):
    FieldType = apps.get_model('designer', 'FieldType')

    start_popup = FieldType()
    start_popup.name = 'Начало всплывающего окна'
    start_popup.machine = 'popup_header'
    start_popup.save()

    end_popup = FieldType()
    end_popup.name = 'Конец всплывающего окна'
    end_popup.machine = 'popup_footer'
    end_popup.save()


class Migration(migrations.Migration):

    dependencies = [
        ('designer', '0003_auto_20150329_1246'),
    ]

    operations = [
        migrations.RunPython(add_popup)
    ]
