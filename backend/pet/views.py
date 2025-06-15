from rest_framework import viewsets

from .models import Pet
from .serializers import PetSerializer


class PetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
