from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from survivor.models import Survivor
from survivor.serializers import SurvivorSerializer

class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def infect(self, request, pk=None):
        return pk
    
    @action(detail=True, methods=['get'])
    def infect(self, request, pk=None):
        return pk