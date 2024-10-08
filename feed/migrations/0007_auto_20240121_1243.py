# Generated by Django 3.0.14 on 2024-01-21 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_auto_20240116_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField(null=True)),
                ('url', models.ImageField(null=True, upload_to='')),
                ('number_of_destinations', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='feed.Category'),
            preserve_default=False,
        ),
    ]
