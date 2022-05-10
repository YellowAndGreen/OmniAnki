# Generated by Django 3.0.4 on 2022-01-12 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0002_auto_20220111_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recitedata',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recitedata', to='flashcards.Card'),
        ),
    ]
