# Generated by Django 3.1.4 on 2020-12-29 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.CharField(default=False, max_length=500, null=True),
        ),
    ]