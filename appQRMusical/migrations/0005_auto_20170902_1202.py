# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-02 10:02
from __future__ import unicode_literals

import appQRMusical.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appQRMusical', '0004_player_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='multimedia',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=appQRMusical.models.directory_to_upload),
        ),
    ]
