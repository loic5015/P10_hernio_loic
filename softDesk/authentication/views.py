from rest_framework import mixins, viewsets
from .serializers import UsersDetailsSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UsersCreateViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = UsersDetailsSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer





