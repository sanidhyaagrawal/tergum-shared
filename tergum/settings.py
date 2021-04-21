import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "*!&w5_h_csw8#uj=u*^hh$dw)-4q56!ty389kiysoa-z!%l#mr"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#"*" means all hosts are allowed. Must change in production.
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    #whitenoise
    "whitenoise.runserver_nostatic",

    #packages
    "django.contrib.sites",   # <--

    #for sign-in with google
    "allauth",   # <--
    "allauth.account",   # <--
    "allauth.socialaccount",   # <--
    "allauth.socialaccount.providers.google",   # <--

    "rest_framework",

    #package to automatically delete the actual files present on
    #the server when it's entry on the databse is deleted.
    #helps to free up server space
    'django_cleanup',

    #apps
    "users", #login-signup related
    "services",
    "profiles",
    "common",
    "payment_gateway", #stripe integration related
    "administrator",
    "employee",
]

AUTHENTICATION_BACKENDS = (
 "django.contrib.auth.backends.ModelBackend",
 "allauth.account.auth_backends.AuthenticationBackend",
 )


#allauth releated settings
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

#suppoerted ISO codes
LANGUAGES = (
('en','English'),
)

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

LOCALE_PATHS = (
os.path.join(BASE_DIR, 'locale/'),
)

ROOT_URLCONF = "tergum.urls"

#frontend template paths
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            os.path.join(BASE_DIR, 'common/frontend/common/templates'),
            os.path.join(BASE_DIR, 'services/frontend/services/templates'),
            os.path.join(BASE_DIR, 'profiles/frontend/admin/templates'),
            os.path.join(BASE_DIR, 'profiles/frontend/customer/templates'),
            os.path.join(BASE_DIR, 'profiles/frontend/employees/templates'),
            os.path.join(BASE_DIR, 'users/frontend/users/templates'),
            os.path.join(BASE_DIR, 'administrator/frontend/administrator/templates'),
            os.path.join(BASE_DIR, 'employee/frontend/employee/templates'),
            os.path.join(BASE_DIR, 'core/frontend/templates'),

        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tergum.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
AUTH_USER_MODEL = "users.User"
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

#API rate limiting
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

#frontend template paths
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/frontend/static'), #base static files
    os.path.join(BASE_DIR, 'common/frontend/common/static'),
    os.path.join(BASE_DIR, 'services/frontend/services/static'),
    os.path.join(BASE_DIR, 'users/frontend/users/static'),
    os.path.join(BASE_DIR, 'profiles/frontend/customer/static'),
    os.path.join(BASE_DIR, 'administrator/frontend/administrator/static'),
    os.path.join(BASE_DIR, 'employee/frontend/employee/static'),

] #directories where the static files are located.

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#path where user uploaded files are stored
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sujatisamaj@gmail.com'
EMAIL_HOST_PASSWORD = 'sus07091969'
