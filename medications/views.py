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


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        order = Order.objects.filter(owner=owner)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        # order = Order.objects.filter(owner=owner)
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Retrieve, update or delete a order instance.
    """
    def get_object(self, request, uuid):
        try:
            order = Order.objects.get(id=uuid)
            if order.owner.user != self.request.user:
                raise PermissionError("You are not allowed to access this medication.")
            return order
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        order = self.get_object(uuid)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        order = self.get_object(uuid)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
    
    
class AdminOrderDetailView(APIView):
    permission_classes = [IsAdminUser]

    """
    Retrieve, update or delete a Order instance.
    """
    def get_object(self, uuid):
        try:
            return Order.objects.get(id=uuid)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        order = self.get_object(uuid)
        serializer = AdminOrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        order = self.get_object(uuid)
        serializer = AdminOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class MedicationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        # medication = owner.medication_set.all()
        medication = Medication.objects.filter(owner=owner).all()
        serializer = MedicationSerializer(medication, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Retrieve, update or delete a medication instance.
    """
    
    def get_object(self, uuid):
        try:
            medication = Medication.objects.get(id=uuid)
            if medication.owner.user != self.request.user:
                raise PermissionError("You are not allowed to access this medication.")
            return medication
        except Medication.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        medication = self.get_object(uuid)
        serializer = MedicationSerializer(medication)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        medication = self.get_object(uuid)
        serializer = MedicationSerializer(medication, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
