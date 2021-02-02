from django.shortcuts import render
from rest_framework.views import APIView, Response
from . import views
from rest_framework import status

# Create user API endpoint
class UserCreateAPIView(APIView):
    """
    Creates an user. If user info is not correct
    then an error code is returned.
    """
    def post(self, request, format="json"):
        """
        Not implemented
        """
        return Response({}, status=status.HTTP_501_NOT_IMPLEMENTED)


# Login user API endpoint