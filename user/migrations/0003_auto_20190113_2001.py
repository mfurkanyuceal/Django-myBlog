# Generated by Django 2.1.4 on 2019-01-13 17:01

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190113_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.ImageField(upload_to=user.models.upload_to, verbose_name='Profil Fotoğrafı'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(blank=True, choices=[('O', 'Diğer'), ('E', 'Erkek'), ('K', 'Kadın')], default=3, max_length=1, verbose_name='Cinsiyet'),
        ),
    ]
