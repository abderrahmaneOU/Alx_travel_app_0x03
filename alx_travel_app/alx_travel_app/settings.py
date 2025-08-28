# Celery Configuration
CELERY_BROKER_URL = "amqp://localhost"  # RabbitMQ broker
CELERY_RESULT_BACKEND = "rpc://"        # optional result backend
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# Django Email Backend (example using console for testing)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-password"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "no-reply@example.com"
