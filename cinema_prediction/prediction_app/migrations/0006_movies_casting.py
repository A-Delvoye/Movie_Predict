# Generated by Django 5.2 on 2025-04-23 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0005_rename_url_image_movies_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='casting',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.2 on 2025-04-23 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction_app', '0005_rename_url_image_movies_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='casting',
            field=models.TextField(blank=True, null=True),
        ),
    ]
