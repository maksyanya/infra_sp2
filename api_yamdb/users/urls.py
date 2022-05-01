# from django.urls import include
# from django.urls import path
# from rest_framework.routers import DefaultRouter

# from users.views import SignupView
# from users.views import TokenView
# from users.views import UserViewSet

# v1_router = DefaultRouter()
# v1_router.register(
#     r'users',
#     UserViewSet,
#     basename='users'
# )

# auth_urls = [
#     path('signup/', SignupView.as_view()),
#     path('token/', TokenView.as_view())
# ]

# urlpatterns = [
#     path('v1/', include(v1_router.urls)),
#     path('v1/auth/', include(auth_urls)),
# ]

# Перенес в API/urls
