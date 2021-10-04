from rest_framework import serializers

from happy_dogs.dogs.models import BoardingVisit


class BoardingVisitSerializer(serializers.ModelSerializer):
    dog = serializers.SlugRelatedField(
        read_only=True,
        slug_field='full_name'
    )

    class Meta:
        model = BoardingVisit
        fields = ['dog', 'start_date', 'end_date']
