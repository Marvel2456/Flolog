from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.models import Client, CustomUser
from django.http import Http404
from accounts.utils import log_activity

# Create your views here.
class AgeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        age = Age.objects.all()
        serializer = AgeSerializer(age, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllergyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        allergy = Allergy.objects.all()
        serializer = AllergySerializer(allergy, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AllergySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class HistoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        history = History.objects.all()
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RiskFactorView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        risk = RiskFactor.objects.all()
        serializer = RiskFactorSerializer(risk, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = RiskFactorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MedicalRecordView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        records = MedicalRecord.objects.filter(owner=owner)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicalRecordDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        owner = MedicalRecord.objects.get(owner=request.user)
        serializer = MedicalRecordSerializer(owner)
        log_activity(request.user, 'Viewed biodata')
        return Response(serializer.data)

    def put(self, request, format=None):
        owner = FamilyHistory.objects.get(owner=request.user)
        serializer = FamilyHistorySerializer(owner)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'Updated biodata')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Retrieve, update or delete a medical records instance.
    """
    # def get_object(self, uuid):
    #     try:
    #         records = MedicalRecord.objects.get(id=uuid)
    #         if records.owner.user != self.request.user:
    #             raise PermissionError("You are not allowed to access this medication.")
    #         return records
    #     except MedicalRecord.DoesNotExist:
    #         raise Http404

    # def get(self, request, uuid, format=None):
    #     records = self.get_object(uuid)
    #     serializer = MedicalRecordSerializer(records)
    #     return Response(serializer.data)

    # def put(self, request, uuid, format=None):
    #     records = self.get_object(uuid)
    #     serializer = MedicalRecordSerializer(records, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicalHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        med_history = MedicalHistory.objects.filter(owner=owner)
        serializer = MedicalHistorySerializer(med_history, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        serializer = MedicalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MedicalHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Retrieve, update or delete a medical records instance.
    """

    def get(self, request, format=None):
        owner = MedicalHistory.objects.get(owner=request.user)
        serializer = MedicalHistorySerializer(owner)
        log_activity(request.user, 'Viewed biodata')
        return Response(serializer.data)

    def put(self, request, format=None):
        owner = MedicalHistory.objects.get(owner=request.user)
        serializer = MedicalHistorySerializer(owner)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'Updated biodata')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def get_object(self, uuid):
    #     try:
    #         med_history = MedicalHistory.objects.get(id=uuid)
    #         if med_history.owner.user != self.request.user:
    #             raise PermissionError("You are not allowed to access this medication.")
    #         return med_history
    #     except MedicalHistory.DoesNotExist:
    #         raise Http404

    # def get(self, request, uuid, format=None):
    #     med_history = self.get_object(uuid)
    #     serializer = MedicalHistorySerializer(med_history)
    #     return Response(serializer.data)

    # def put(self, request, uuid, format=None):
    #     med_history = self.get_object(uuid)
    #     serializer = MedicalHistorySerializer(med_history, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PatientAllergyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        allergy = Allergy.objects.filter(owner=owner)
        serializer = PatientAllergySerialier(allergy, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        serializer = PatientAllergySerialier(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AllergyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    """
    Retrieve, update or delete a medical records instance.
    """

    def get(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        allergy = PatientAllergy.objects.get(owner=owner)
        serializer = PatientAllergySerialier(allergy, many=True)
        log_activity(request.user, 'Viewed biodata')
        return Response(serializer.data)

    def put(self, request, format=None):
        # owner = Client.objects.get(user=request.user)
        owner = PatientAllergy.objects.get(owner=request.user)
        serializer = PatientAllergySerialier(owner)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'Updated biodata')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def get_object(self, uuid):
    #     try:
    #         allergy = PatientAllergy.objects.get(id=uuid)
    #         if allergy.owner.user != self.request.user:
    #             raise PermissionError("You are not allowed to access this medication.")
    #         return allergy
    #     except Allergy.DoesNotExist:
    #         raise Http404

    # def get(self, request, uuid, format=None):
    #     allergy = self.get_object(uuid)
    #     serializer = PatientAllergySerialier(allergy)
    #     return Response(serializer.data)

    # def put(self, request, uuid, format=None):
    #     allergy = self.get_object(uuid)
    #     serializer = PatientAllergySerialier(allergy, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FamilyHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, formant=None):
        owner = Client.objects.get(user=request.user)
        family = FamilyHistory.objects.filter(owner=owner)
        serializer = FamilyHistorySerializer(family, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        owner = Client.objects.get(user=request.user)
        serializer = FamilyHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class FamilyHistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        owner = FamilyHistory.objects.get(owner=request.user)
        serializer = FamilyHistorySerializer(owner)
        log_activity(request.user, 'Viewed biodata')
        return Response(serializer.data)

    def put(self, request, format=None):
        owner = FamilyHistory.objects.get(owner=request.user)
        serializer = FamilyHistorySerializer(owner)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'Updated biodata')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class AdminMedicalRecordView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        records = MedicalRecord.objects.all()
        serializer = AdminMedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AdminMedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class AdminMedicalRecordDetailView(APIView):
    permission_classes = [IsAdminUser]

    """
    Retrieve, update or delete a Medication instance.
    """
    def get_object(self, uuid):
        try:
            return MedicalRecord.objects.get(id=uuid)
        except MedicalRecord.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        records = self.get_object(uuid)
        serializer = AdminMedicalRecordSerializer(records)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        records = self.get_object(uuid)
        serializer = AdminMedicalRecordSerializer(records, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminMedicalHistoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        med_history = MedicalHistory.objects.all()
        serializer = AdminMedicalHistorySerializer(med_history, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AdminMedicalHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class AdminMedicalHistoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    """
    Retrieve, update or delete a Medication instance.
    """
    def get_object(self, uuid):
        try:
            return MedicalHistory.objects.get(id=uuid)
        except MedicalHistory.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        med_history = self.get_object(uuid)
        serializer = AdminMedicalHistorySerializer(med_history)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        med_history = self.get_object(uuid)
        serializer = AdminMedicalHistorySerializer(med_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AdminAllergyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        allergy = PatientAllergy.objects.all()
        serializer = AdminAllergySerialier(allergy, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AdminAllergySerialier(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class AdminAllergyDetailView(APIView):
    permission_classes = [IsAdminUser]

    """
    Retrieve, update or delete a Medication instance.
    """
    def get_object(self, uuid):
        try:
            return PatientAllergy.objects.get(id=uuid)
        except PatientAllergy.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        allergy = self.get_object(uuid)
        serializer = AdminAllergySerialier(allergy)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        allergy = self.get_object(uuid)
        serializer = AdminAllergySerialier(allergy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdminFamilyHistoryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, formant=None):
        family = FamilyHistory.objects.all()
        serializer = AdminFamilyHistorySerializer(family, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AdminFamilyHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
class AdminFamilyHistoryDetailView(APIView):
    permission_classes = [IsAdminUser]

    """
    Retrieve, update or delete a Medication instance.
    """
    def get_object(self, uuid):
        try:
            return FamilyHistory.objects.get(id=uuid)
        except FamilyHistory.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        family = self.get_object(uuid)
        serializer = AdminFamilyHistorySerializer(family)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        family = self.get_object(uuid)
        serializer = AdminFamilyHistorySerializer(family, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

