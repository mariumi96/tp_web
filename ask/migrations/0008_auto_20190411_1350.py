# Generated by Django 2.1.7 on 2019-04-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0007_auto_20190411_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='next_q1',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='next_q2',
            field=models.IntegerField(default='1'),
        ),
    ]
