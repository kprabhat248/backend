# backend/core/settings.py

import os
from pathlib import Path
import dj_database_url ### --- IMPORT: Added for flexible database configuration ---

BASE_DIR = Path(__file__).resolve().parent.parent

### --- SECRET_KEY: Made dynamic for production ---
# Gets the secret key from an environment variable. If not found, uses the insecure dev key.
# Render will generate a secure key for you.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-this-is-a-dev-key-so-its-ok')

### --- DEBUG: Made dynamic for production ---
# Reads from an environment variable. Defaults to 'True' for local development.
# The '== "True"' comparison is important because environment variables are strings.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

### --- ALLOWED_HOSTS: Configured for production deployment ---
# This list is empty by default.
ALLOWED_HOSTS = []
# Render sets the RENDER_EXTERNAL_HOSTNAME environment variable. We add it to our hosts.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Also allow localhost for local development
if DEBUG:
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd Party Apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    # Local Apps
    'users',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', ### --- MIDDLEWARE: Added Whitenoise for serving static files ---
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.debug', 'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'core.wsgi.application'

### --- DATABASE: Made dynamic for production ---
# This will use Render's PostgreSQL in production (via the DATABASE_URL env var)
# and your local SQLite for development if the env var is not set.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'

# This is the logic that separates your local setup from Render's setup.
if DEBUG:
    # --- LOCAL DEVELOPMENT SETTINGS ---
    # When running locally (DEBUG=True), media files are stored in a simple 'media' folder in your project.
    # This makes them easy to find and manage during development.
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # --- RENDER (PRODUCTION) SETTINGS ---
    # When running on Render (DEBUG=False), media files will be saved to a temporary directory.
    # Note: These files will be DELETED on every deploy, as the /tmp/ directory is not persistent.
    MEDIA_ROOT = '/tmp/media'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': ['rest_framework.parsers.JSONParser', 'rest_framework.parsers.FormParser', 'rest_framework.parsers.MultiPartParser'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

SPECTACULAR_SETTINGS = {'TITLE': 'App Points API', 'DESCRIPTION': 'API for app points service.', 'VERSION': '1.0.0'}

### --- CORS: Made dynamic for production ---
# These are the default origins for local development.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]

# You can add your deployed Netlify frontend URLs in Render as a comma-separated
# environment variable named 'CORS_ALLOWED_ORIGINS_DEPLOYED'.
if 'CORS_ALLOWED_ORIGINS_DEPLOYED' in os.environ:
    # Get the comma-separated string from the env var and split it into a list
    deployed_origins = os.environ['CORS_ALLOWED_ORIGINS_DEPLOYED'].split(',')
    # Add the cleaned origins to the allowed list
    CORS_ALLOWED_ORIGINS.extend([origin.strip() for origin in deployed_origins])