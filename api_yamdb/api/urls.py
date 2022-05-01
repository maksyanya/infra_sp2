from django.urls import include, path

from rest_framework import routers

from api.views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                       ReviewsViewSet, TitleViewSet)
from users.views import SignupView, TokenView, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

router_v1.register(r'categories', CategoryViewSet, basename='category')
router_v1.register(r'genres', GenreViewSet, basename='genre')
router_v1.register(r'titles', TitleViewSet, basename='title')

router_v1.register(r'users', UserViewSet, basename='users')

auth_urls = [
    path('signup/', SignupView.as_view()),
    path('token/', TokenView.as_view())
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
