# Generated by Django 2.1.4 on 2018-12-28 23:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20181229_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(help_text='İçerik giriniz', verbose_name='İçerik'),
        ),
    ]