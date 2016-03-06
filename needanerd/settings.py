LINKED_IN_URL = 'www.linkedin.com'
LINKED_IN_API_URL = 'api.linkedin.com'
LINKED_IN_API_KEY = '77ec2qizij7hrp'
LINKED_IN_SECRET_KEY = '8sCUZ28BGhWYFY99'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '77ec2qizij7hrp'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = '8sCUZ28BGhWYFY99'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:8888/'
SOCIAL_AUTH_LOGIN_URL = '/'

#Default session is one hour unless the user hits the "Remember Me" Button
SESSION_COOKIE_AGE=3600

# a setting to determine whether we are running on OpenShift
IN_DOCKER = False
#if os.environ.has_key('OPENSHIFT_REPO_DIR'):
#    ON_OPENSHIFT = True
    
#if ON_OPENSHIFT:
    #I am exclusively using this in the .py files. In the templates there is a {{BASE_URL}} given from the context processors to provide the status
    #This app is currently using Django 1.6 but in Django 1.7 you would not need to set a variable, you can use request.scheme()+request.get_host()
#    HOST = 'https://non-josborne.rhcloud.com'
#else:
HOST = 'http://localhost:8888'
    
APPEND_SLASH = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.office365.com'
EMAIL_HOST_USER = 'JFO0002@tigermail.auburn.edu'
EMAIL_HOST_PASSWORD = 'hqzwpbbffzyphals' #Gmail App Password, cannot sign into Gmail with this password but can use SMTP
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEBUG = True

EMAIL_SUBJECT_PREFIX="NeedaNerd"
ADMINS = (
    ('John Osborne', 'JFO0002@auburn.edu'),
)

MANAGERS = ADMINS

if IN_DOCKER:
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'nan_db',
            'USER': 'nerd',
            'PASSWORD': 'AuburnUniversity2016!',
            'HOST': '$DB_PORT_5432_TCP_ADDR',                      
            'PORT': '$DB_PORT_5432_TCP_PORT',
        }
    }
    
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'nan_db',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django.core.context_processors.request",
                "needanerd.context_processors.baseurl",
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uxefyg6)j**w0b1t=9w(1#r+(z4s89#@9fgcdse7kq*#yf$$lt'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'needanerd.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'needanerd.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'appsecurity',
    'student',
    'employer',
    'job',
    'msgcenter',
    'needanerd',
    'resume',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    #'bootstrap3',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.linkedin.LinkedinOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simpletime': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'logging.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simpletime'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'], #was 'mail_admins'
            'level': 'ERROR',
            'propagate': True,
        },
         'NeedANerd.custom': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
           
           
}
