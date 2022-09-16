from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]
