import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"WebSocket CONNECTED: {self.room_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f"WebSocket DISCONNECTED: {self.room_name}, Code: {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message', '')

            # Ignore empty messages
            if not message.strip():
                return

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON format"}))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
