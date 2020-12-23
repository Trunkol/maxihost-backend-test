from .models import User
from rest_framework import viewsets, permissions
from users.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    