import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Nhận tên phòng từ URL (có thể tùy chỉnh)
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        # Tham gia nhóm chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Chấp nhận kết nối WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Rời khỏi nhóm chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Nhận tin nhắn từ WebSocket và gửi đi cho tất cả người tham gia phòng chat
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Gửi tin nhắn vào nhóm chat
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Gửi tin nhắn tới WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))