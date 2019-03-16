# Generated by Django 2.1.4 on 2018-12-28 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_post_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='exit', editable=False, max_length=122, unique=True, verbose_name='Slug Alanı'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, help_text='Resim Dosyası Yükleyebilirsiniz', upload_to='', verbose_name='Fotoğraf'),
        ),
    ]