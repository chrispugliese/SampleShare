import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat  # Import the Message and Chat models

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'chat_{self.room_name}'

		# Check if user is authenticated
		if not self.scope["user"].is_authenticated:
			await self.close()
			return

		# Check if user is a member of the chat
		try:
			chat = await Chat.objects.get(chatName=self.room_name)
			if not chat.userProfiles.filter(user=self.scope["user"]).exists():
				await self.close()
				return
		except Chat.DoesNotExist:
			await self.close()
			return

		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()


	async def disconnect(self, close_code):
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message_text = text_data_json['message']
		user = self.scope["user"]  # Get the user from the scope

		# Save the message to the database
		chat = Chat.objects.get(chatName=self.room_name)  # Fetch the chat instance
		Message.objects.create(chat=chat, user=user, message=message_text)  # Save the message

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message_text
			}
		)

	async def chat_message(self, event):
		message = event['message']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'message': message
		}))
