# Generated by Django 3.0.4 on 2022-03-09 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0015_settings_current_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='recitedata',
            name='last_params',
            field=models.CharField(default='[]', max_length=20000),
        ),
    ]
