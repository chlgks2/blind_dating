from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """WebSocket 연결 시 쿼리스트링의 token으로 JWT 인증"""
    async def __call__(self, scope, receive, send):
        query = parse_qs(scope['query_string'].decode())
        token = query.get('token', [None])[0]

        if token:
            try:
                access = AccessToken(token)
                scope['user'] = await get_user(access['user_id'])
            except Exception:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
