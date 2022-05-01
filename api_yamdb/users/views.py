from django.contrib.auth.tokens import (PasswordResetTokenGenerator,
                                        default_token_generator)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.permissions import IsAdmin
from users.serializers import SignupSerializer, TokenSerializer, UserSerializer

TOKEN_CODE = PasswordResetTokenGenerator()


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    user_mail = [user.email]
    site_email = 'YaMDb@yandex.ru'
    message = 'Your confirm code:'
    return send_mail(message, confirmation_code,
                     site_email, user_mail, fail_silently=False)


class SignupView(APIView):
    """Регистрация нового пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            email=serializer.validated_data['email'],
            username=serializer.validated_data['username'],
        ).first()
        if not user:
            if User.objects.filter(
                email=serializer.validated_data['email'],
            ).exists() or User.objects.filter(
                username=serializer.validated_data['username']
            ).exists() or (serializer.validated_data['username'] == 'me'):
                # Test. Добавил игнор 'me' при создании.
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                is_active=False
            )
        if not user.is_active:
            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Получение JWT-токена."""
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)

        if TOKEN_CODE.check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response(
            {f'This confirm code: {confirmation_code} is invalid code!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """ Управление пользователями."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    serializer_class = UserSerializer
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)

        return Response(serializer.data)
