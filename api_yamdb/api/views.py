from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .permissions import IsAuthorModeratorAdminOrReadOnlyPermission, IsAdminUserOrReadOnly

from .serializers import (ReviewSerializer, CommentSerializer,
                          GenreSerializer, CategorySerializer,
                          TitleSerializerGet, TitlSerializerPost)

from reviews.models import Title, Review, Category, Genre


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission, )
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(raiting=Avg('reviews__score')).all()
    permission_classes = (IsAdminUserOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializerGet
        return TitlSerializerPost


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnlyPermission,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
