from rest_framework.serializers import ModelSerializer
from titles.models import Category, Genre, Title


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
