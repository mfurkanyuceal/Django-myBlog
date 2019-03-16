# Generated by Django 2.1.4 on 2019-01-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20190115_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[('O', 'Diğer'), ('E', 'Erkek'), ('K', 'Kadın')], default=3, max_length=1, verbose_name='Cinsiyet'),
        ),
    ]
