from medifam_serv_project.persons.models import Man, Woman
from rest_framework.response import Response
from .serializers import ManSerializer, WomanSerializer
from django.shortcuts import render
from rest_framework import views, generics
from rest_framework.request import Request
from rest_framework import status

# Create your views here.
class CreateManApiView(views.APIView):
    def post(self, request: Request, format="json"):
        man = ManSerializer(data=request.data)
        if man.is_valid():
            man.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(man.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateWomanApiView(views.APIView):
    def post(self, request: Request, format="json"):
        woman = WomanSerializer(data=request.data)
        if woman.is_valid():
            woman.save()
            return Response({}, status=status.HTTP_201_CREATED)
        return Response(woman.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterPersonApiView(generics.ListAPIView):
    def get_queryset(self):
        gender = self.kwargs["gender"]
        if gender == "woman":
            # Do filtering against Woman model
            try:
                return Woman.objects.filter(**self.request.query_params)
            except:
                print("Error filtering")
        else:
            # Do filtering against Man model
            try:
                return Man.objects.filter(**self.request.query_params)
            except:
                print("error filtering")