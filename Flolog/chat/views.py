from django.shortcuts import render
from accounts.models import Client, Pharmacist, CustomUser
from .models import Chatroom
from .serializers import ChatroomSerializer, MessageSerializer
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .pusher import pusher_client
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class RequestChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        client = Client.objects.get(user=request.user)

        if client.coin > 0:
            # Deduct 1 token from the client's wallet
            client.coin -= 1
            client.save()

            # Create a new Chatroom instance
            chatroom = Chatroom.objects.create(client=client)

            

            serializer = ChatroomSerializer(chatroom)
            return Response({
                'chatroom': serializer.data,
                
               
            })
        else:
            return Response({"error": "Insufficient tokens in the wallet."}, status=400)
        

class ViewChatRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            pharmacist = Pharmacist.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response(data={"error": "Pharmacist not found."}, status=404)
        
        chat_requests = Chatroom.objects.filter(is_active=True, pharmacist=None)
        serializer = ChatroomSerializer(chat_requests, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            pharmacist = Pharmacist.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response(data={"error": "Pharmacist not found."}, status=400)
        
        chatroom_id = request.data.get('chatroom_id')

        chatroom = Chatroom.objects.get(id=chatroom_id)

        # Add pharmacist to room with no pharmacy
        if chatroom.is_active and chatroom.pharmacist is None:
            chatroom.pharmacist = pharmacist
            chatroom.save()

            pharmacist_data = serializers.serialize('json', [pharmacist])
            # Trigger an event indicating a pharmacist has joined the chatroom
            pusher_client.trigger('chatroom-channel', 'pharmacist-joined', {
                # 'chatroom_id': chatroom.id,
                'pharmacist': pharmacist_data,
            })

            return Response(data={"success": "You have joined the chatroom."})

        elif chatroom.is_active and chatroom.pharmacist == pharmacist:
            # End the chat and close the chatroom
            chatroom.close_chat()

            # Trigger for the closure of the chatroom
            pusher_client.trigger('chatroom-channel', 'chatroom-closed', {'chatroom_id': chatroom_id})

            # Reward the pharmacist with 500 naira in the wallet
            pharmacist.balance += 500
            pharmacist.save()

            # Return success response indicating the pharmacist has joined the chatroom
            return Response(data={"success": "You successfully closed the chatroom."})
        else:
            # Return error response indicating the chatroom is no longer available
            return Response(data={"error": "Chatroom is no longer available."}, status=400)
        

class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            chatroom_id = request.data.get('room')
            chatroom = Chatroom.objects.get(id=chatroom_id)
            serializer.save(room=chatroom, sender=request.user)

            message_data = serializer.data
            message_data['timestamp'] = str(message_data['timestamp'])
            message_data['sender'] = str(request.user.email)
            message_data['room'] = str(message_data['room'])

            pusher_client.trigger('chat-channel', 'new-message', message_data)

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


