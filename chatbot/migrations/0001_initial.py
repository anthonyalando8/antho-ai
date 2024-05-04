# Generated by Django 5.0.2 on 2024-05-04 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=12000)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_id', models.CharField(blank=True, max_length=100, null=True)),
                ('current_history', models.TextField()),
                ('date', models.DateField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chathistory', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.CharField(max_length=100, null=True)),
                ('message', models.CharField(max_length=30000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('response', models.CharField(max_length=5000)),
                ('date', models.DateTimeField()),
                ('chatHistory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.chathistory')),
            ],
        ),
    ]
