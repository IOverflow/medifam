from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import serializers, status
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User

# Create user API endpoint
class UserCreateAPIView(APIView):
    """
    Creates an user. If user info is not correct
    then an error code is returned.
    """

    def post(self, request: Request, format="json"):
        """
        Description:
        -----------
        Endpoint for registering a new user on the system.
        
        Return codes:
        ------------
        On sucess: 201 (Created)

        On faliure: 400 (BAD Request)
        """
        serializer = UserSerializer(data=request.data)
        # Check data sanity
        if serializer.is_valid():
            # Commit user to DB
            user = serializer.save()
            if user:
                # Generate user token for authentication
                token = Token.objects.create(user=user)
                json = serializer.data
                json["token"] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)