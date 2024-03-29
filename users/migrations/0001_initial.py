# Generated by Django 4.2.7 on 2024-01-31 04:43

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import users.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'Bu username allaqachon mavjud'}, help_text='harf, raqam va @/./+/-/_. lardan foydalaning. 32ta belgidan oshmasin', max_length=32, unique=True, validators=[users.models.UnicodeUsernameValidator()], verbose_name='username')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('picture', models.ImageField(blank=True, default='users/profile_pics/user-default-pic.png', help_text='Rasm hajmi 0.7mb dan oshmasligi kerak. Iloji borija kvadrat rasm yuklashga harakat qiling', null=True, upload_to='users/profile_pics/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'avif', 'bmp', 'webp', 'svg', 'heic', 'heif', 'tiff', 'tif', 'bmp', 'gif'], message='iltimos faqat rasm yuklang va hajmi 0.7mb dan oshmasligi kerak'), users.models.validate_file_size])),
                ('bio', models.TextField(blank=True, max_length=256, null=True)),
                ('ommaviy', models.BooleanField(default=True, help_text="Siz ko'rgan, yoqtirgan va saqlagan filmlaringizni boshqalar ham ko'ra oladi!!")),
                ('second_id', models.IntegerField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
