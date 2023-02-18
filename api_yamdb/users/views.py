from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core.mail import send_mail
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .permissions import (
    AdminOnly, AdminOrReadOnly,
    AuthorOrReadOnly, ModeratorOrReadOnly
)
from random import randint
from .serializers import (
    SignUpSerializer, TokenSerializer, CustomUserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    http_method_names = ["get", "post", "delete", "patch"]

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        if request.method == 'GET':
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        serializer.save()


class SignUp(APIView):
    def post(self, request):
        try:
            user = CustomUser.objects.get(
                username=request.data['username'],
                email=request.data['email']
            )
            serializer = SignUpSerializer(user, data=request.data)
        except Exception:
            serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = str(randint(100000, 999999))
        serializer.save(confirmation_code=code)
        ndata = serializer.validated_data
        user = CustomUser.objects.get(username=ndata['username'])
        send_mail(
            'Код для вашей регистрации',
            f'Код: {code}',
            'api_yamdb@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ndata = serializer.validated_data
        user = get_object_or_404(CustomUser, username=ndata['username'])
        if ndata['confirmation_code'] == user.confirmation_code:
            refresh = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(refresh)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )