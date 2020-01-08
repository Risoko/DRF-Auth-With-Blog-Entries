# Generated by Django 3.0.1 on 2020-01-08 08:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog_auth', '0003_auto_20200108_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(default=django.utils.timezone.now, help_text='Enter the publication date of the article.', verbose_name='publish date')),
                ('like', models.SmallIntegerField(default=0, verbose_name='you like it')),
                ('dislike', models.SmallIntegerField(default=0, verbose_name='you dislike it')),
                ('title', models.CharField(help_text='Enter title.', max_length=300, validators=[django.core.validators.MinLengthValidator(limit_value=10)], verbose_name='title')),
                ('entry', models.TextField(help_text='Your blog entry', validators=[django.core.validators.MinLengthValidator(limit_value=200)], verbose_name='blog entry')),
                ('for_adult', models.BooleanField(default=False, verbose_name='adult content')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog_auth.User')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateField(default=django.utils.timezone.now, help_text='Enter the publication date of the article.', verbose_name='publish date')),
                ('content_comment', models.CharField(help_text='Comment for entry blog.', max_length=400, validators=[django.core.validators.MinLengthValidator(limit_value=10)], verbose_name='comment')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog_entries.Article')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog_auth.User')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ['-pub_date'],
            },
        ),
    ]