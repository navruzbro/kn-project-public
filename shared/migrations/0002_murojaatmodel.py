# Generated by Django 4.2.7 on 2024-02-01 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MurojaatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('body', models.TextField(blank=True, max_length=300, null=True)),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='murojaat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
