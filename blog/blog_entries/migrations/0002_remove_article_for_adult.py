# Generated by Django 3.0.1 on 2020-01-08 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_entries', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='for_adult',
        ),
    ]
