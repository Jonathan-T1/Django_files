# Generated by Django 4.2.2 on 2023-10-23 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning', '0002_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fotouser',
            field=models.ImageField(blank=True, null=True, upload_to='Media/'),
        ),
    ]
