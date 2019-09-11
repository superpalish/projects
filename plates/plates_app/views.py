from rest_framework import viewsets

# Create your views here.
from plates_app.models import NumberPlate
from plates_app.serializers import NumberPlateSerializer


class NumberPlateViewSet(viewsets.ModelViewSet):
    queryset = NumberPlate.objects.all()
    serializer_class = NumberPlateSerializer
