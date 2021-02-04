from django.contrib.auth.models import User
from rest_framework import exceptions, serializers
import django.contrib.auth.password_validation as pass_validator
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        validators=[UniqueValidator(User.objects.all())],
        max_length=32,
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_password(self, data):
        numerics = "1234567890"
        upper_case = "abcdefghijklmnopqrstuvwxyz".upper()
        syms = "_,./;'][\\=-)(*&^%$#@!<>?:}{|"
        errors = dict()
        messages = []
        if all(x not in data for x in numerics):
            messages += "Must contain at least a numeric character"
        if all(x not in data for x in upper_case):
            messages += "Must contain at least an upper case character"
        if all(x not in data for x in syms):
            messages += "Must contain a non-alphanumeric character"

        if messages:
            errors["password"] = messages
            raise serializers.ValidationError(errors)

        return data

    def validate(self, data):
        user = User(**data)
        password = data.get("password")
        errors = dict()

        try:
            pass_validator.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
