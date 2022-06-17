import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CategoriesGenresMixins
from .permissions import IsAdmin, IsAdminModeratorAuthorOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ProfileSerializer, ReviewSerializer,
                          SignUpSerializer, TitleSerializer,
                          TitleViewSerializer, TokenSerializer, UserSerializer)


def get_confirmation_code_and_send_mail(user):
    confirmation_code = uuid.uuid5(uuid.NAMESPACE_OID, user.__str__())
    subject = 'Код подтверждения'
    message = (
        f'username: {user.username}, confirmation_code: {confirmation_code}'
    )
    return send_mail(subject, message, None, (user.email, ))


@api_view(['POST'])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    get_confirmation_code_and_send_mail(user)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
def token_view(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.data.get('confirmation_code')
    uuid_code = str(uuid.uuid5(uuid.NAMESPACE_OID, user.__str__()))
    if uuid_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        return Response(
            {'Ваш токен': str(refresh.access_token)}, status=HTTP_200_OK
        )
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, )
    ordering = ('username', )
    filter_backends = (SearchFilter, )
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    search_fields = ('username', )

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated, )
    )
    def about_me(self, request):
        serializer = ProfileSerializer(request.user)
        if request.method == 'PATCH':
            serializer = ProfileSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)


class CategoryViewSet(CategoriesGenresMixins):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)


class GenreViewSet(CategoriesGenresMixins):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('name')
    filterset_class = TitleFilter
    permission_classes = (ReadOnly | IsAdmin,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleViewSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
