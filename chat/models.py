from django.db import models
from accounts.models import CustomUser, Client, Pharmacist
import uuid
from django.utils import timezone
from biodata.models import MedicalHistory, MedicalRecord, FamilyHistory, PatientAllergy

# Create your models here.




# class Message(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return f"{self.sender.email} - {self.timestamp}"



class Chatroom(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, blank=True, null=True)
    med_records = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, blank=True, null=True)
    med_history = models.OneToOneField(MedicalHistory, on_delete=models.CASCADE, blank=True, null=True)
    allergy = models.OneToOneField(PatientAllergy, on_delete=models.CASCADE, blank=True, null=True)
    fam_history = models.OneToOneField(FamilyHistory, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def close_chat(self):
        self.is_active = False
        self.end_time = timezone.now()
        self.save()

    def __str__(self) -> str:
        return f"{self.client} - {self.end_time}"
    

class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    room = models.ForeignKey(Chatroom, on_delete=models.PROTECT, blank=True, null=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sender.email} - {self.timestamp}"
