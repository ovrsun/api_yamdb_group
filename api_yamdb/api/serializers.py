from rest_framework.serializers import ModelSerializer, SlugRelatedField
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review, Comment


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


class ReviewSerializer(ModelSerializer):
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise ValidationError('Оценка от 1 до 10')
        return value

    def validate(self, value):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filters(title=title, author=author).exists()
        ):
            raise ValidationError('Отзыв можно сделать один раз')
        return value

    class Meta:
        models = Review
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    review = SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        models = Comment
        fields = '__all__'
