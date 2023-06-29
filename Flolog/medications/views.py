from django.shortcuts import render
from .serializers import *
from .models import*
from accounts.models import Client
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.

class MedicationCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = MedicationSerializer(data=request.data)

        if serializer.is_valid():
            medication = serializer.save()
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

   
class AdminMedicationDetailView(APIView):
    permission_classes = [IsAdminUser]

    """
    Retrieve, update or delete a Medication instance.
    """
    def get_object(self, uuid):
        try:
            return Medication.objects.get(id=uuid)
        except Medication.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        medications = self.get_object(uuid)
        serializer = AdminMedicationSerializer(medications)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        medications = self.get_object(uuid)
        serializer = AdminMedicationSerializer(medications, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
