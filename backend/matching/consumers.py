import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Match, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f'chat_{self.match_id}'

        # 인증 안 됐거나, 내 채팅방이 아니면 거부
        if self.user.is_anonymous:
            await self.close()
            return
        if not await self.is_participant():
            await self.close()
            return

        # 그룹(방)에 참가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """클라이언트 → 서버 메시지 수신"""
        data = json.loads(text_data)
        content = data.get('content', '').strip()
        if not content:
            return

        # DB 저장
        msg = await self.save_message(content)

        # 같은 방의 모든 연결에 브로드캐스트
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',   # 아래 chat_message 메서드 호출
                'message': {
                    'id': msg['id'],
                    'sender_nickname': msg['sender_nickname'],
                    'content': msg['content'],
                    'created_at': msg['created_at'],
                },
            }
        )

    async def chat_message(self, event):
        """그룹 → 각 클라이언트로 전송"""
        await self.send(text_data=json.dumps(event['message']))

    # === DB 작업 (동기 → 비동기 래핑) ===
    @database_sync_to_async
    def is_participant(self):
        try:
            match = Match.objects.get(id=self.match_id)
        except Match.DoesNotExist:
            return False
        # 당사자 + 채팅 오픈(둘 다 결제) 상태여야 함
        is_member = self.user == match.user_a or self.user == match.user_b
        return is_member and match.is_chat_open   # ← 결제 조건 추가

    @database_sync_to_async
    def save_message(self, content):
        match = Match.objects.get(id=self.match_id)
        msg = Message.objects.create(
            match=match, sender=self.user, content=content
        )
        return {
            'id': msg.id,
            'sender_nickname': self.user.nickname,
            'content': msg.content,
            'created_at': msg.created_at.isoformat(),
        }
