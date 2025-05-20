import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Media files directory for storing extracted figures
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Create media directory if it doesn't exist
os.makedirs(os.path.join(MEDIA_ROOT, 'figures'), exist_ok=True)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-key-for-development-only")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
if os.getenv("ALLOWED_HOSTS"):
    ALLOWED_HOSTS += os.getenv("ALLOWED_HOSTS").split(",")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "axes",
    # Local apps
    "api",
    "api.analytics.apps.AnalyticsConfig",  # Analytics subapp
    "api.auth.apps.AuthConfig",  # Auth subapp
    "api.security.apps.SecurityConfig",  # Security subapp
    "api.quality.apps.QualityConfig",  # Quality subapp
    "api.feedback.apps.FeedbackConfig",  # Feedback subapp
    "api.search.apps.SearchConfig",  # Search subapp
]

# Configure axes to use the database backend for persistent lockouts
AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list
    'axes.backends.AxesStandaloneBackend',
    # Django's default ModelBackend for model-based authentication
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "api.security.error_handling.SecurityMiddleware",  # Security error handling (must be first)
    "api.security.headers.SecurityHeadersMiddleware",  # Security headers
    "api.security.waf.WAFMiddleware",  # Web Application Firewall protection
    "api.security.middleware.PIIFilterMiddleware",  # PII detection and filtering
    "api.security.rate_limiting.RateLimitingMiddleware",  # API rate limiting
    "api.security.connection.ConnectionTimeoutMiddleware",  # Connection timeout enforcement
    "axes.middleware.AxesMiddleware",  # Login attempt tracking and brute force protection
    "api.analytics.middleware.AnalyticsMiddleware",  # Analytics data collection
]

# Configure django-axes behind reverse proxy
AXES_PROXY_COUNT = 1  # Number of proxies in front of the application
AXES_META_PRECEDENCE_ORDER = [
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
]

# PII Detection and filtering settings
SCAN_REQUESTS_FOR_PII = True
SCAN_RESPONSES_FOR_PII = False  # Enable only in high-security environments
AUTO_REDACT_PII = False  # Set to True to automatically redact detected PII
MAX_PII_SCAN_SIZE = 5 * 1024 * 1024  # 5MB maximum file size for PII scanning

# Rate limiting settings
ENABLE_RATE_LIMITING = True
RATE_LIMIT_DEFAULT = "60/minute"  # Default rate limit for all API endpoints
RATE_LIMIT_EXEMPTIONS = []  # List of exempted IPs or user IDs
RATE_LIMIT_RULES = {
    "/api/query/": "30/minute",  # Main search query endpoint
    "/api/search/": "40/minute",  # General search endpoint
    "/api/auth/login/": "10/minute",  # Login attempts
    "/api/auth/register/": "5/hour",  # Registration attempts
    "/api/upload/": "10/hour",  # Document uploads
}
RATE_LIMIT_BLOCK_DURATION = 300  # 5 minutes block for limit violations
RATE_LIMIT_ANALYTICS = True  # Log rate limit events

# Web Application Firewall (WAF) settings
WAF_ENABLED = False  # Enable WAF protection
WAF_EXCLUDED_PATHS = [
    '/admin/',      # Admin panel has its own security
    '/static/',     # Static files don't need WAF protection
    '/media/',      # Media files don't need WAF protection
    '/health/',     # Health check endpoint (doesn't contain user input)
]
WAF_SECURITY_LEVEL = 'low'  # Options: 'low', 'medium', 'high'
WAF_BLOCK_IP_DURATION = 600  # 10 minutes block for repeated attacks
WAF_MAX_VIOLATIONS = 3  # Number of violations before blocking IP

# Connection security settings
ENABLE_CONNECTION_TIMEOUT = True
CONNECTION_TIMEOUT_SECONDS = 1800  # 30 minutes of inactivity
CONNECTION_CLEANUP_INTERVAL = 300  # 5 minutes between cleanup runs
MAX_CONNECTIONS_PER_IP = 10  # Maximum simultaneous connections per IP

# Differential privacy settings
ENABLE_DP_EMBEDDING_PROTECTION = True  # Enable differential privacy for embeddings
DP_EPSILON = 0.1  # Privacy parameter (lower = more privacy)
DP_SENSITIVITY = 0.1  # L2 sensitivity of embeddings
DP_CLIP_NORM = 1.0  # Maximum L2 norm for clipping
DP_NOISE_MECHANISM = 'gaussian'  # 'gaussian' or 'laplace'

# Security headers settings
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')
SECURITY_HEADERS_MONITORING = True
CSP_CONFIG = {
    "default-src": ["'self'"],
    "img-src": ["'self'", "data:"],
    "script-src": ["'self'", "'unsafe-inline'"],  # Unsafe-inline needed for React
    "style-src": ["'self'", "'unsafe-inline'"],  # Unsafe-inline needed for React
    "connect-src": ["'self'", "localhost:*"],
    "font-src": ["'self'"],
    "frame-src": ["'none'"],
    "object-src": ["'none'"],
    "base-uri": ["'self'"],
    "form-action": ["'self'"],
}

ROOT_URLCONF = "rna_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "rna_backend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Check if we should use SQLite (set by docker-entrypoint.sh)
USE_SQLITE = os.getenv("USE_SQLITE", "False") == "True"

if USE_SQLITE:
    print("Using SQLite database for development/fallback")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    print("Using PostgreSQL database")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "rna_db"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Celery settings
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"  # Golden rule #4

# Backup settings
BACKUP_RETENTION_DAYS = int(os.getenv("BACKUP_RETENTION_DAYS", "7"))
BACKUP_CLEANUP_LOCAL = os.getenv("BACKUP_CLEANUP_LOCAL", "False") == "True"
AWS_BACKUP_BUCKET = os.getenv("AWS_BACKUP_BUCKET", "")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT", "")

# Cache settings (used for rate limiting)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Weaviate settings
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")

# Weaviate mTLS settings
WEAVIATE_TLS_ENABLED = os.getenv("WEAVIATE_TLS_ENABLED", "False") == "True"
WEAVIATE_CLIENT_CERT = os.getenv("WEAVIATE_CLIENT_CERT", "")
WEAVIATE_CLIENT_KEY = os.getenv("WEAVIATE_CLIENT_KEY", "")
WEAVIATE_CA_CERT = os.getenv("WEAVIATE_CA_CERT", "")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "30"))

# LLM network isolation settings
LLM_NETWORK_ISOLATION = os.getenv("LLM_NETWORK_ISOLATION", "False") == "True"
LLM_FORCE_ISOLATION = os.getenv("LLM_FORCE_ISOLATION", "False") == "True"
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3:8b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "60"))

# Local embedding model settings
LOCAL_EMBEDDING_MODEL_PATH = os.getenv("LOCAL_EMBEDDING_MODEL_PATH", "")
LOCAL_EMBEDDING_TOKENIZER_PATH = os.getenv("LOCAL_EMBEDDING_TOKENIZER_PATH", "")
LOCAL_EMBEDDING_DIMENSION = int(os.getenv("LOCAL_EMBEDDING_DIMENSION", "768"))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for demo
CORS_ALLOWED_ORIGINS = ['http://localhost:5173']  # Vite dev server
if os.getenv("CORS_ALLOWED_ORIGINS"):
    CORS_ALLOWED_ORIGINS += os.getenv("CORS_ALLOWED_ORIGINS").split(",")

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # Changed for demo purposes
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "30/minute",
        "user": "60/minute",
    },
    "EXCEPTION_HANDLER": "api.security.error_handling.custom_exception_handler",
}

# Chunking settings (Golden rule #1)
CHUNK_SIZE = 400
CHUNK_OVERLAP = 100

# Analytics settings
ANALYTICS_ENABLED = True
ANALYTICS_RETENTION_DAYS = 90  # Days to keep raw analytics data
ANALYTICS_MONITOR_SYSTEM = True  # Enable system performance monitoring
ANALYTICS_SENSITIVE_PATHS = [
    '/admin/',
    '/api/auth/',
    '/api/users/',
]  # Paths containing sensitive operations to audit

# JWT Authentication settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=15),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    
    # Security enhancements
    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
}

# Django-Axes for login security
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5  # Number of failed login attempts before lockout
AXES_LOCK_OUT_AT_FAILURE = True  # Lock out user after failed login attempts
AXES_COOLOFF_TIME = 1  # Lock out for 1 hour (in hours)
AXES_LOCKOUT_TEMPLATE = None  # No custom template, return 403 response
AXES_LOCKOUT_URL = None  # No custom lockout URL
AXES_RESET_ON_SUCCESS = True  # Reset failed login attempts after successful login
AXES_USE_USER_AGENT = True  # Track user agent to prevent bypass of lockout
AXES_CACHE = 'default'  # Use the default cache for tracking login attempts
AXES_HANDLER = 'axes.handlers.cache.AxesCacheHandler'  # Use cache handler for storage