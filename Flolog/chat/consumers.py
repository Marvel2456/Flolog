from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Chatroom, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtain the chatroom ID from the URL or query parameters
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']

        # Add the consumer to a specific chat group based on the chatroom ID
        await self.channel_layer.group_add(
            str(self.chatroom_id),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove the consumer from the chat group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            str(self.chatroom_id),
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages from the WebSocket
        message = json.loads(text_data)
        # message = text_data_json['message']
        content = message.get('content', '')
        
        if content == 'end_chat':
            chatroom = Chatroom.objects.get(id=self.chatroom_id)

            if chatroom.is_active and chatroom.pharmacist is not None:
                # Set the chatroom as inactive and save it
                chatroom.is_active = False
                chatroom.save()

                # Broadcast the chat closing message to the chat group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'content': 'Chat closed by the pharmacist.'
                    }
                )
                return

        # Broadcast the received message to the chat group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': content
            }
        )
        

    async def chat_message(self, event):
        # Send the chat message to the WebSocket connection
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))