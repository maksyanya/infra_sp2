from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.custom_viewset import ListOrCreateOrDestroy
from api.filters import TitleFilter
from api.permissions import (IsAdminOrReadOnlyPermission,
                             IsAuthorOrReadOnlyOrAdminOrModerator)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleCreateSerializer, TitleSerializer)
from reviews.models import Category, Genre, Review, Title


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnlyOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        if Review.objects.filter(title=title,
                                 author=self.request.user).exists():
            raise serializers.ValidationError('ERROR_DUBPLICATE_REVIEW')
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyOrAdminOrModerator,
                          IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(ListOrCreateOrDestroy):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination


class GenreViewSet(ListOrCreateOrDestroy):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['category', 'genre', 'name', 'year']
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer
