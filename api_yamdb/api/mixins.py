from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class CategoriesGenresMixins(CreateModelMixin, ListModelMixin,
                             DestroyModelMixin, GenericViewSet):
    pass
