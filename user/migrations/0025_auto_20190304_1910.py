# Generated by Django 2.1.4 on 2019-03-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_auto_20190304_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[('O', 'Diğer'), ('E', 'Erkek'), ('K', 'Kadın')], default=3, max_length=1, verbose_name='Cinsiyet'),
        ),
    ]
