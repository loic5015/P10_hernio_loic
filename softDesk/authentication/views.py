from rest_framework import mixins, viewsets
from .serializers import UsersDetailsSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from project.serializers import UserSerializer
from project.permissions import IsAuthorize
from .models import Users


class UsersCreateViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        Endpoint for create a new user
    """

    serializer_class = UsersDetailsSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UsersListViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
           Endpoint for list all the users of the app. User must be authenticated
    """
    queryset = Users.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAuthorize]
