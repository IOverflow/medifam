from .models import Man, Person, Woman
from rest_framework.response import Response
from .serializers import ManSerializer, WomanSerializer
from django.shortcuts import render
from rest_framework import views, generics
from rest_framework.request import Request
from rest_framework import status
from django_filters import rest_framework as filters

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
    queryset = Person.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)

    def get(self, request: Request, *args, **kwargs):
        return Response({}, status.HTTP_501_NOT_IMPLEMENTED)