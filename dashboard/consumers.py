import asyncio
import json
from random import *
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from users.models import Profile
from dashboard.models import Payment
from users.models import User
from uuid import uuid4
from .models import Group


class UserConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.room_name = self.scope['url_route']['room_name']
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        print("Connected", event)
        await self.send(
            {
                "type": "websocket.accept"
            }
        )
    
    async def websocket_disconnect(self, event):
        #Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
    
    async def websocket_receive(self, event):
        print("Receive", event)
        data = json.loads(event['text'])

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "update",
                "text": data['id']
            }
        )
    
    async def update(self, event):
        id = event['text']
        user = await self.get_user(id)
        profile = user.profile
        count = await self.get_count(profile)
        await self.send({
            "type": "websocket.send",
            "text": count 
        })


    @database_sync_to_async
    def get_user(self, id):
        user =  User.objects.get(id=id)
        return user

    @database_sync_to_async
    def get_count(self, profile):
        children_count = profile.child_of.all().count()
        grandchildren_count = profile.grand_child_of.all().count()
        return children_count + grandchildren_count


class UniversalConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.room_name = 'universal'
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
       
        print("Connected", event)

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_disconnect(self, event):
        #Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
    #Receive message from websocket
    async def websocket_receive(self,event):
    
        data = json.loads(event['text'])
        print("receive", event)
        #Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': data['action'],
                'message': data['id']
            }
           
        )

    #Receive message from group
    async def chat_message(self, event):
        print("message", event)
        await self.send({
                'type': 'websocket.send',
                "text": event['message']
            })
    
    async def update(self, event):
        #The user has to send the id for us to identify the user
        id = event['message']
        user = await self.get_user(id)
        await self.create_group(user)
        if user.profile.is_new:
            await self.modify_user_profile(user)
        print(user.username)
        data = await self.get_data()
        data['user'] = user.username
        data['action'] = 'registered'
        await self.send({
            'type': 'websocket.send',
            "text": json.dumps(data)
        })

    async def fetch(self, event):
        pass
    
    async def notify(self, event):
        print("Notify", event)
        data = await self.get_data();
        id = event['message']
        user = await self.get_user(id)
        data['user'] = user.username
        data['action'] = 'withdrawed'
        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(data)
        })

    @database_sync_to_async
    def create_group(self,user):
        Group.objects.create(name=user.username,user=user.profile)

    @database_sync_to_async
    def get_user(self, id):
        user =  User.objects.get(id=id)
        return user


    @database_sync_to_async
    def get_data(self):
        active_count = Profile.objects.filter(is_active=True).count()
        not_active_count = Profile.objects.filter(is_active=False).count()
        level1_count = Profile.objects.filter(level=1).count()
        level2_count = Profile.objects.filter(level=2).count()
        users_count = Profile.objects.count()
        payments_count = Payment.objects.count()
        pending_payments = Payment.objects.filter(completed=False).count()
        completed_payments = Payment.objects.filter(completed=True).count()
        data = {
            'active': active_count,
            'not_active':not_active_count,
            'level1': level1_count,
            'level2': level2_count,
            'users': users_count,
            'completed': completed_payments,
            'payments': payments_count,
            'pending': pending_payments
        }
        return data
    

    @database_sync_to_async
    def modify_user_profile(self,user):

        parent = user.profile.is_child_of
        grandparent = user.profile.is_grand_child_of
            
        if parent.child_of.all().count() == 2:
                parent.level = 1
                parent.save()
        if grandparent.grand_child_of.all().count() == 4:
                grandparent.level = 2
                grandparent.can_withdraw = True
                grandparent.save()
    
        profile = Profile.objects.get(user=user)
        profile.is_new = False
        profile.save()