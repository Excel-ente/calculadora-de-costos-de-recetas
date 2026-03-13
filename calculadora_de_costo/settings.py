import os
from pathlib import Path
from dotenv import load_dotenv
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga el archivo .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

MODO_DESARROLLO = os.getenv('MODO_DESARROLLO') == 'True'

SECRET_KEY = os.getenv('SECRET_KEY')

if MODO_DESARROLLO:
    DEBUG = True
else:
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

if MODO_DESARROLLO:
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = []
else:
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'import_export',
    'administracion', 
    'configuracion',
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

ROOT_URLCONF = 'calculadora_de_costo.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'calculadora_de_costo.wsgi.application'

if MODO_DESARROLLO:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': os.getenv('DB_PATH', os.path.join(BASE_DIR, 'db.sqlite3')),
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

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT=os.path.join(BASE_DIR, 'staticfiles')

# Media files (Uploads)
# https://docs.djangoproject.com/en/5.1/topics/files/
if MODO_DESARROLLO:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
else:
    MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
    MEDIA_URL = os.getenv('MEDIA_URL', '/media/')

# Aumenta el límite de campos para formularios con muchos inputs (import-export, etc.)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

JAZZMIN_SETTINGS = {
    
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Calculadora de Costos de Recetas",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Calculadora de Costos de Receta",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Calculadora",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "logo.png",  # Django busca automáticamente en STATIC_URL

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "logo.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": "logo.png",

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",  # Opciones: "img-circle" (redondo) o quitar para rectangular
    
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "logo.png",  # Ícono que aparece en la pestaña del navegador

    # Welcome text on the login screen
    "welcome_sign": "Calculadora de Costos de Recetas - Excel-Ente",

    # Copyright on the footer
    "copyright": "Esta herramienta la trae EXCEL-ENTE en colaboración con ADEMA Sistemas.",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": [],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############


    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Configuracion", "url": "/admin/configuracion/configuracion/", "new_window": False, "icon": "fas fa-cog"},
        {"name": "Ayuda", "url": "https://ademasistemas.com", "new_window": True , "icon":"fas fa-question-circle"},
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ['auth',],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": ['pedidos.ItemPedido','administracion.Categoria','administracion.CategoriaReceta','administracion.ProductoReceta','configuracion.Configuracion'],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        'dashboard',
        'pedidos',
        'administracion',
        'agenda',
    ],

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",

        'dashboard.DashboardConfig': "fas fa-tachometer-alt",
        "administracion.Categoria": "fas fa-list-alt",
        "administracion.Producto": "fas fa-carrot",
        "administracion.CategoriaReceta": "fas fa-list",
        "administracion.Receta": "fas fa-book", 
        "administracion.ProductoReceta": "fas fa-american-sign-language-interpreting", 
        "administracion.Bien": "fas fa-kitchen-set",

    },

    "topmenu_links": [
        {"app": "administracion", "collapsible": True, "icon": "fas fa-app"},
    ],

    # Links personalizados en el sidebar (debajo de la app)
    "custom_links": {
        "administracion": [
            {
                "name": "Importar / Exportar Productos",
                "url": "importar_exportar_productos",
                "icon": "fas fa-file-excel",
            },
            {
                "name": "Importar / Exportar Recetas",
                "url": "importar_exportar_recetas",
                "icon": "fas fa-file-import",
            },
        ]
    },

    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
 
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs",
        "pedidos.pedido": "single",
        },
    

    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-pink",
    "accent": "accent-maroon",
    "navbar": "navbar-pink navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-maroon",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": True,
    "theme": "minty",
    "dark_mode_theme": "solar",
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": True
}