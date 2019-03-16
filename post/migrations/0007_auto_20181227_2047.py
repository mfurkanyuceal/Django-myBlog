# Generated by Django 2.1.4 on 2018-12-27 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_auto_20181227_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(help_text='Kategori seçimi yapınız', related_name='post', to='post.Category', verbose_name='Kategoriler'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(help_text='İçerik giriniz', verbose_name='İçerik'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Başlık giriniz', max_length=120, verbose_name='Başlık'),
        ),
    ]
