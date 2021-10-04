import factory


class DogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dogs.Dog'

    first_name = factory.Faker('name')


class BoardingVisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'dogs.BoardingVisit'

    dog = factory.SubFactory(DogFactory)
