from pathlib import Path
# weather_django/settings.py
INSTALLED_APPS = [
    

    'weather',
]
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',     
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Add at bottom
API_KEY = '32875eb42ebaa5659423d3501dc9d75c'
ALLOWED_HOSTS = ['*']  # Allow all hosts for development purposes
ROOT_URLCONF = 'weather.urls'