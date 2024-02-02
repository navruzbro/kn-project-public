# Generated by Django 4.2.7 on 2024-01-31 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('film', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmlike',
            name='saved',
        ),
        migrations.AlterField(
            model_name='filmmodel',
            name='active',
            field=models.BooleanField(default=True, help_text="vaqtinchalik o'chirib qo'yish mumkin ...."),
        ),
        migrations.AlterField(
            model_name='filmmodel',
            name='slug',
            field=models.SlugField(blank=True, help_text='Bunga hech narsa yozma!!!!', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='FilmSaved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved', models.BooleanField(default=False)),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to='film.filmmodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saved', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
