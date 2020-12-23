from django.db import IntegrityError, transaction
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from survivor.models import Survivor, InfectedSurvivor
from survivor.serializers import SurvivorSerializer
from .permissions import IsOwnerOrReadOnly


class SurvivorViewSet(viewsets.ModelViewSet):
    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    @action(detail=True, methods=['POST'])
    @transaction.atomic
    def infect(self, request, pk=None):
        try:
            survivor_infected = Survivor.objects.get(pk=pk)
        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reported_by = Survivor.objects.filter(user=request.user).first()
        
        try:
            InfectedSurvivor.objects.create(reported_by=reported_by, 
                                            survivor_infected=survivor_infected)
            survivor_infected.evaluate_infection()
        except IntegrityError:
            return Response(data={'error':"This user already reported this survivor"}, 
                            status=status.HTTP_412_PRECONDITION_FAILED)

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'])
    def closest(self, request, pk=None):
        try:
            survivor = Survivor.objects.get(pk=pk)
        except Survivor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        return Response(data=survivor.get_nearest(), status=status.HTTP_200_OK)
