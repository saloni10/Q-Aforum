# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QAforum', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
