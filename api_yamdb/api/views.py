# from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet

from titles.models import Category, Genre, Title
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
