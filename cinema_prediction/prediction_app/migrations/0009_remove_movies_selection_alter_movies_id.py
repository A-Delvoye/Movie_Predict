# Generated by Django 5.2 on 2025-04-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0008_alter_movies_genre_alter_movies_selection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='selection',
        ),
        migrations.AlterField(
            model_name='movies',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
