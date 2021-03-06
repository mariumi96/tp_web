# Generated by Django 2.1.7 on 2019-04-02 19:58

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0004_auto_20190402_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogBreed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('desc', models.TextField()),
                ('voice', models.IntegerField(choices=[(0, 'silent'), (1, 'normal'), (2, 'loud')], default=0)),
                ('wool', models.IntegerField(choices=[(0, 'none'), (1, 'short'), (2, 'medium'), (3, 'long')], default=0)),
                ('size', models.IntegerField(choices=[(0, 'small'), (1, 'medium'), (2, 'big')], default=0)),
                ('temper', multiselectfield.db.fields.MultiSelectField(choices=[(0, 'calm'), (1, 'kind'), (2, 'loyal'), (3, 'playful')], default=0, max_length=7)),
                ('points', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Порода собаки',
                'verbose_name_plural': 'Породы собак',
            },
        ),
        migrations.AlterField(
            model_name='dog',
            name='breed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ask.DogBreed'),
        ),
    ]
