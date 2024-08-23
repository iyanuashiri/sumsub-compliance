from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import transaction, IntegrityError

from rest_framework import serializers

from sumsubapp.accounts.constants import Message
from sumsubapp.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email', 'is_active')


class AccountCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    default_error_messages = {
        "cannot_create_user": Message.CANNOT_CREATE_USER_ERROR.value
    }

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def validate(self, attrs):
        user = Account(attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                account = Account.objects.create_user(**validated_data)
                account.is_active = True
                account.save(update_fields=["is_active"])
        except IntegrityError:
            self.fail("cannot_create_user")

        return account


class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, required=False)
    email = serializers.EmailField()

    default_error_messages = {
        "invalid_credentials": Message.INVALID_CREDENTIALS_ERROR.value,
        "inactive_account": Message.INACTIVE_ACCOUNT_ERROR.value,
    }

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")

        account = authenticate(request=self.context.get("request"), email=email, password=password)
        if not account:
            account = Account.objects.filter(email=email).first()
            if account and not account.check_password(password):
                self.fail("invalid_credentials")
        if account and account.is_active:
            attrs['user'] = account
            return attrs
        self.fail("invalid_credentials")
