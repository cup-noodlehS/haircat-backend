import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from asgiref.sync import sync_to_async

User = get_user_model()

# In-memory storage for active connections
# Structure: {user_id: {client_id: WebSocketConsumer}}
connections = {}

@sync_to_async
def get_user_from_token_sync(token):
    """Get user from JWT token string (synchronous version)"""
    try:
        auth = JWTAuthentication()
        validated_token = auth.get_validated_token(token)
        user = auth.get_user(validated_token)
        return user
    except (InvalidToken, TokenError):
        return None

async def get_user_from_token(token):
    """Get user from JWT token string (async wrapper)"""
    return await get_user_from_token_sync(token)

class WebhookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the token from the query parameters
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        token_param = None
        
        # Parse query string manually
        params = query_string.split('&')
        for param in params:
            if param.startswith('token='):
                token_param = param.replace('token=', '')
                break
                
        if not token_param:
            await self.close()
            return
            
        self.user = await get_user_from_token(token_param)
        
        if not self.user:
            await self.close()
            return
            
        self.user_id = str(self.user.id)
        self.client_id = self.scope['client'][0] + '_' + str(self.scope['client'][1])
        
        # Register this connection
        if self.user_id not in connections:
            connections[self.user_id] = {}
        connections[self.user_id][self.client_id] = self
        
        # Add user to a group
        self.group_name = f"user_{self.user_id}"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        # Remove this connection
        if hasattr(self, 'user_id') and hasattr(self, 'client_id'):
            if self.user_id in connections and self.client_id in connections[self.user_id]:
                del connections[self.user_id][self.client_id]
                if not connections[self.user_id]:
                    del connections[self.user_id]
                
            # Remove from the group
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        # We don't expect to receive data from clients
        # But you could implement it if needed
        pass
        
    async def webhook_event(self, event):
        # Send webhook event to connected websocket
        await self.send(text_data=json.dumps({
            'event': event['event'],
            'data': event['data']
        }))

# Utility function to send webhook events
def send_webhook(event_name, user_id, data):
    """
    Send a webhook event to a specific user
    
    Args:
        event_name (str): Name of the event
        user_id (str): User ID to send the event to
        data (dict): Data to send with the event
    
    Returns:
        bool: True if event was sent, False otherwise
    """
    from asgiref.sync import async_to_sync
    from channels.layers import get_channel_layer
    
    channel_layer = get_channel_layer()
    group_name = f"user_{user_id}"
    
    try:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'webhook_event',
                'event': event_name,
                'data': data
            }
        )
        return True
    except Exception as e:
        print(f"Failed to send webhook: {e}")
        return False 