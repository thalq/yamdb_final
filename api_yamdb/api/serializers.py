from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField, StringRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'username "me" использоватье нельзя'
            )
        return value


class UserSerializer(SignUpSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ProfileSerializer(UserSerializer):
    role = StringRelatedField(read_only=True)


class TokenSerializer(serializers.Serializer):
    username = CharField()
    confirmation_code = CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title

    @staticmethod
    def validate_year(value):
        current_year = timezone.now().year
        if 1896 > value > current_year:  # '1896 первый показ Прибытия поезда'
            raise ValidationError('Год выпуска не может быть больше текущего.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='name',
                                         read_only=True,)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        if 10 < data['score'] < 1:
            raise ValidationError('Оценка не может быть ниже 1'
                                  'или выше 10')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    review = serializers.SlugRelatedField(slug_field='text',
                                          read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'review')
        model = Comment
