# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('caption', models.CharField(max_length=500)),
                ('color', models.CharField(max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Nominee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('rating', models.DecimalField(default=1500, max_digits=7, decimal_places=2)),
                ('rating_deviation', models.DecimalField(default=350, max_digits=7, decimal_places=2)),
                ('last_updated', models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0), auto_now=True)),
                ('category', models.ForeignKey(to='bestof.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
