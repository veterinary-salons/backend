from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from authentication.email_messages import (
    FROM_EMAIL, RECOVERY_CODE_SUBJECT, RECOVERY_CODE_MESSAGE,
)
from authentication.permissions import EmailCodeConfirmed
from authentication.v1.serializers import (
    SignUpProfileSerializer, RecoveryEmailSerializer, 
    RecoveryCodeSerializer, RecoveryPasswordSerializer,
    SignInSerializer,
)
from authentication.utils import get_recovery_code, send_email_message
from core.exceptions import InvalidRequestData
from core.constants import Limits
from users.v1.serializers import (
    CustomerProfileSerializer, SupplierProfileSerializer,
)


class SignUpViewSet(viewsets.GenericViewSet):
    http_method_names = ("post",)
    allowed_methods = ("POST",)
    serializer_class = SignUpProfileSerializer

    def get_queryset(self):
        return None

    def create(self, request):
        full_serializer = self.get_serializer(data=request.data)
        full_serializer.is_valid(raise_exception=True)
        profile_type = full_serializer.validated_data.pop("profile_type")
        if profile_type == "customer":
            serializer = CustomerProfileSerializer(
                data=full_serializer.validated_data
            )
        elif profile_type == "supplier":
            serializer = SupplierProfileSerializer(
                data=full_serializer.validated_data
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.validated_data, status=HTTP_201_CREATED
        )

    """
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=IsAuthenticated,
    )
    def verify_email(self, request):
        user = request.user
        verification_code = str(request.data.get("code", None))
        email_hash = str(md5_hash(user.email))
        if (
            verification_code == "None" or
            len(verification_code) != Limits.CONFIRMATION_CODE_LENGTH or
            verification_code != email_hash[:Limits.CONFIRMATION_CODE_LENGTH]
        ):
            raise InvalidRequestData("invalid code")
        user.email_confirmed = True
        user.save()
        return Response(
            data={"message": "email confirmed"}, 
            status=HTTP_200_OK
        )
        """


class SignInViewSet(viewsets.GenericViewSet):
    http_method_names = ("post",)
    allowed_methods = ("POST",)

    def _perform_data_validation(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "create":
            return SignInSerializer
        elif self.action == "recovery":
            return RecoveryEmailSerializer
        elif self.action == "recovery_code":
            return RecoveryCodeSerializer
        elif self.action == "recovery_password":
            return RecoveryPasswordSerializer

    def create(self, request):
        return self._perform_data_validation(request)

    @action(
        methods=("POST",),
        detail=False,
    )
    def recovery(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        recovery_code = get_recovery_code(email)
        message = RECOVERY_CODE_MESSAGE.format(code=recovery_code.code)
        send_email_message(
            subject=RECOVERY_CODE_SUBJECT, 
            message=message, 
            sender=FROM_EMAIL,
            recipients=[email],
        )
        return Response(data=serializer.validated_data, status=HTTP_200_OK)

    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def recovery_code(self, request):
        return self._perform_data_validation(request)

    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(IsAuthenticated, EmailCodeConfirmed),
    )
    def recovery_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.validated_data, status=HTTP_200_OK)