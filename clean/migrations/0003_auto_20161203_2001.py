# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clean', '0002_uploadeddata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
