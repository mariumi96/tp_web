# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-11 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0007_auto_20180111_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='uploads/avatars/avatar.png', upload_to='uploads/avatars/'),
        ),
    ]
