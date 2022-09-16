from djoser.views import UserViewSet

from apps.users.models import CustomUser
from apps.users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
