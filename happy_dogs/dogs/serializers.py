from rest_framework.serializers import ModelSerializer

from happy_dogs.dogs.models import BoardingVisit


class BoardingVisitSerializer(ModelSerializer):
    class Meta:
        model = BoardingVisit
        fields = ['dog', 'start_date', 'end_date']
