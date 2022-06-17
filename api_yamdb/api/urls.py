from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, signup_view,
                       token_view)

from django.urls import include, path

from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='ftitles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', signup_view, name='signup'),
    path('v1/auth/token/', token_view, name='token'),
    path('v1/', include(router_v1.urls)),
]
