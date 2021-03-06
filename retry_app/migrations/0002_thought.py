# Generated by Django 2.2.4 on 2020-09-21 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retry_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thoughts', to='retry_app.User')),
                ('users_who_like', models.ManyToManyField(related_name='liked_thoughts', to='retry_app.User')),
            ],
        ),
    ]
