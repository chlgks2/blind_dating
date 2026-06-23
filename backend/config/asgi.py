import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Django 앱을 먼저 초기화 (모델 import 전에 필요)
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from matching.middleware import JWTAuthMiddleware   # 아래에서 만듦
import matching.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(
        URLRouter(matching.routing.websocket_urlpatterns)
    ),
})
