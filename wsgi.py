import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_sales_may_2024-main.settings')

application = get_wsgi_application()
