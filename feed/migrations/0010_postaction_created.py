# Generated by Django 3.0.14 on 2024-04-10 15:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0009_post_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='postaction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
