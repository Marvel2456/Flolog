from django.shortcuts import render
from .serializers import *
from .models import*
from accounts.models import ClientProfile
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        owner = ClientProfile.objects.get(user=request.user)
        order = Order.objects.filter(owner=owner)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        owner = ClientProfile.objects.get(user=request.user)
        # order = Order.objects.filter(owner=owner)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class AdminOrderView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        order = Order.objects.all()
        serializer = AdminOrderSerializer(order, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AdminOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class MedicationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        owner = ClientProfile.objects.get(user=request.user)
        # medication = owner.medication_set.all()
        medication = Medication.objects.filter(owner=owner).all()
        serializer = MedicationSerializer(medication, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        owner = ClientProfile.objects.get(user=request.user)
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminMedicationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        medication = Medication.objects.all()
        serializer = AdminMedicationSerializer(medication, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AdminMedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        