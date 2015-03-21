# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
                ('title', models.CharField(max_length=60)),
                ('date_created', models.DateField(max_length=30)),
                ('date_update', models.DateField(max_length=50)),
                ('is_anonymous', models.BooleanField(verbose_name=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
