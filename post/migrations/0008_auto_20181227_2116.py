# Generated by Django 2.1.4 on 2018-12-27 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20181227_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
