import re
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=False, max_length=150, allow_blank=True)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise DjangoValidationError("A user with that email already exists.")
        return email

    def save(self, request):
        email = self.validated_data.get("email")

        username_generated = re.sub("[^A-Za-z0-9]+", "", email.split("@")[0])
        original_username = username_generated
        count = 1
        while User.objects.filter(username=username_generated).exists():
            username_generated = f"{original_username}{count}"
            count += 1

        self.validated_data["username"] = username_generated

        user = super().save(request)
        return user
