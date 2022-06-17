from api.validators import validate_year

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField('Биография', max_length=600, blank=True)
    role = models.CharField('Роль',
                            max_length=30,
                            choices=ROLE_CHOICES,
                            default=USER,
                            blank=True)

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN


class Category(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.SmallIntegerField('год', validators=(validate_year,))
    description = models.TextField(
        'описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField('текст')
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True
    )
    score = models.IntegerField('оценка',
                                validators=[MinValueValidator(0),
                                            MaxValueValidator(10)])
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        )

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)
