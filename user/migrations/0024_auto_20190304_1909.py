# Generated by Django 2.1.4 on 2019-03-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_auto_20190227_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[('K', 'Kadın'), ('O', 'Diğer'), ('E', 'Erkek')], default=3, max_length=1, verbose_name='Cinsiyet'),
        ),
    ]
