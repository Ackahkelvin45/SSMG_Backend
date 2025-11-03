from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import (
    UserViewSet,
    ServiceViewSet
)

app_name = 'authentication'

# Create a DRF router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    # JWT Authentication endpoints
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Include the automatically generated CRUD routes
    path('', include(router.urls)),
]
