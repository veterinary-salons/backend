import hashlib

from icecream import ic
from hashlib import md5 as md5_hash
from rest_framework import viewsets, serializers, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from api.v1.serializers.authentication import (
    SignUpProfileSerializer,
    SignInSerializer,
    RecoveryEmailSerializer,
    RecoveryCodeSerializer,
    RecoveryPasswordSerializer,
    BasicProfileInfoSerializer,
)
from api.v1.serializers.users import (
    SupplierProfileSerializer,
    CustomerProfileSerializer,
)
from authentication.email_messages import (
    FROM_EMAIL,
    RECOVERY_CODE_SUBJECT,
    RECOVERY_CODE_MESSAGE,
)
from authentication.models import EmailCode
from authentication.permissions import IsEmailConfirmed
from authentication.utils import get_recovery_code, send_email_message
from core.constants import Limits
from core.exceptions import InvalidRequestData


class SignUpView(generics.CreateAPIView):

    serializer_class = SignUpProfileSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return None

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        code = get_recovery_code(email).code
        send_email_message(
            subject="Подтвердите email",
            message=f"Ваш код: {code}",
            sender=FROM_EMAIL,
            recipients=[email],
        )
        full_serializer = self.get_serializer(data=request.data)
        full_serializer.is_valid(raise_exception=True)
        profile_type = full_serializer.validated_data.get("profile_type")

        if profile_type == "customer":
            serializer = CustomerProfileSerializer(
                data=full_serializer.validated_data,
                context = {"request": request},
            )
        elif profile_type == "supplier":
            serializer = SupplierProfileSerializer(
                data=full_serializer.validated_data,
                context = {"request": request},
            )
        else:
            raise serializers.ValidationError(
                "Неправильный тип профиля, только `customer` или `supplier`"
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.to_representation(serializer.validated_data),
            status=HTTP_201_CREATED,
        )

class VerifyEmailView(generics.GenericAPIView):
    serializer_class = BasicProfileInfoSerializer
    permission_classes=[IsAuthenticated,]

    def post(self, request):
        email = request.user.email
        verification_code = request.data.get("code")
        
        try:
            email_code = EmailCode.objects.get(email=email)
            if email_code.code == verification_code:
                request.user.email_confirmed = True
                request.user.save()
                return Response({"message": "Email verified"}, status=HTTP_200_OK)
            else:
                raise serializers.ValidationError("Invalid code")
        
        except EmailCode.DoesNotExist:
            raise serializers.ValidationError("No verification code exists for this email")


class SignInViewSet(viewsets.GenericViewSet):
    http_method_names = ("post",)
    allowed_methods = ("POST",)

    @staticmethod
    def _perform_data_validation(request):
        serializer =SignInSerializer(
        data=request.data,
        context={'request': request},
    )
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
        authentication_classes=(),
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
        permission_classes=(IsAuthenticated, IsEmailConfirmed),
    )
    def recovery_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.validated_data, status=HTTP_200_OK)

    @action(
        methods=("POST",),
        detail=False,
        permission_classes=(IsAuthenticated, IsEmailConfirmed),
    )
    def recovery_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.validated_data, status=HTTP_200_OK)
