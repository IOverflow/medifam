from django.db.models import query
from .filters import PersonFilterSet
from .models import Man, Person, Woman
from rest_framework.response import Response
from .serializers import ManSerializer, PersonSerializer, WomanSerializer
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


class RetrieveWomanApiView(generics.RetrieveAPIView):
    lookup_field = "dni"
    serializer_class = WomanSerializer
    queryset = Woman.objects.all()


class RetrieveManApiView(generics.RetrieveAPIView):
    lookup_field = "dni"
    serializer_class = ManSerializer
    queryset = Man.objects.all()


class RetrievePersonApiView(generics.RetrieveAPIView):
    lookup_field = "dni"
    serializer_class = PersonSerializer
    queryset = Man.objects.all()


class FilterPersonApiView(generics.ListAPIView):
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PersonFilterSet

    def get_queryset(self):
        queryset = Person.objects.none()
        gender = self.kwargs.get("gender", None)
        if gender:
            if gender == "man":
                queryset = Man.objects.all()
            elif gender == "woman":
                queryset = Woman.objects.all()
            else:
                queryset = Person.objects.all()
        return queryset

    def get_serializer_class(self):
        gender = self.kwargs.get("gender", None)
        if gender:
            if gender == "man":
                return ManSerializer
            elif gender == "woman":
                return WomanSerializer
            else:
                return PersonSerializer
        return super().get_serializer_class()