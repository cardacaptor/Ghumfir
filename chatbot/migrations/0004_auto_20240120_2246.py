# Generated by Django 3.0.14 on 2024-01-20 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_auto_20240116_2158'),
        ('chatbot', '0003_auto_20240120_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagepost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommended_post', to='feed.Post'),
        ),
    ]
