"""
Kinomakon project...
Bu NavruzBRO tomonidan qurilgan yirik loyiha
Contact us : mailto:navruznorpulatov@gmail.com
"""

from decouple import config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


#SECRET KEY
SECRET_KEY = config('SECRET_KEY')


#SECRET
DEBUG = config('DEBUG', default=False, cast=bool)

#SECURITY

ALLOWED_HOSTS = ['kinomakon.uz','www.kinomakon.uz','https://kinomakon.uz', 'http://kinomakon.uz',   'localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #packages
    'hitcount',

    #Custom apps
    'film',
    'users',
    'shared',
    'filmnews',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #add with me
                #FILMS
                'film.context_processor.davlatlar',
                'film.context_processor.yillar',
                'film.context_processor.janrlar',
                'film.context_processor.kinoolamdef',
                'film.context_processor.base',
                #FILMNEWS
                'filmnews.context_filmnews.filmnews',
                #USERS
                'users.context_users.users',
                #END add with me

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
        'USER': config('DB_USER'),
        'PASSWORD':config('DB_PASSWORD'),

    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Vaqt sozlamalari o'zbekiston vaqtiga to'g'irlangan
LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

#My Static Files
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

#My Media files
MEDIA_ROOT  = 'media'
MEDIA_URL = '/media/'

#My User Model
AUTH_USER_MODEL = 'users.CustomUser'

#redirect Login (but we have signup)
LOGIN_URL = 'users:signup'




#Version control

#first create --> 1.0
#date == 02 fevral 2024
#version == 1.0
#rating == Big, create
#comment == '''''BU kinomakon web loyihasining ilk versiyasi chunki
# ---------------- kinomakon web sayti birinchi marta taqdim etilmoqda.
# ---------------- Kinomakon asl kelib chiqishi esa 2022yil oxirida
# ---------------- boshlangan edi va 2023yil yanvar oyida faoliyatini
# ---------------- boshlagan edi. endi esa 1yildan so'ng Kinomakon o'z web
# ---------------- saytini ishga tushirdi. Bundan buyog'iga to'xtash yo'q.
# ---------------- O'sishda davom etamiz ''''''


#Next update
#date ==
#version ==
#rating ==
#comment ==