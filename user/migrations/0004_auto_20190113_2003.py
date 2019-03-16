# Generated by Django 2.1.4 on 2019-01-13 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190113_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[('K', 'Kadın'), ('O', 'Diğer'), ('E', 'Erkek')], default=3, max_length=1, verbose_name='Cinsiyet'),
        ),
    ]