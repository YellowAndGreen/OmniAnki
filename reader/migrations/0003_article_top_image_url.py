# Generated by Django 3.0.4 on 2022-03-03 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_auto_20220302_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='top_image_url',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
