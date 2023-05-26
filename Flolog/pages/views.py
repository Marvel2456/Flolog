from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Pharmacist

# Create your views here.

class HomeView(APIView):

    def get(self, request,*args, **kwargs):
        code = str(kwargs.get('ref_code'))
        try:
            pharma = Pharmacist.objects.get(referral_code=code)
            request.session['ref_profile'] = str(pharma.id)
            print('id', pharma.id)
        except:
            pass
        return Response("Welcome")