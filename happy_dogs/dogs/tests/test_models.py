import pytest
from datetime import date

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from pytest_factoryboy import register

from happy_dogs.dogs.factories import DogFactory, BoardingVisitFactory

register(DogFactory)
pytestmark = pytest.mark.django_db


def test_unique_dog_visit_fail(dog):
    with pytest.raises(ValidationError):
        start_date = date(2021, 10, 1)
        end_date = date(2021, 10, 10)
        visit_one = BoardingVisitFactory(
            dog=dog, start_date=date(2021, 10, 1), end_date=date(2021, 10, 11)
        )
        visit_two = BoardingVisitFactory.build(
            dog=dog, start_date=date(2021, 10, 2), end_date=date(2021, 10, 12)
        )
        visit_two.clean()


def test_unique_dog_visit_ok(dog):
    visit_one = BoardingVisitFactory(
        dog=dog, start_date=date(2021, 10, 1), end_date=date(2021, 10, 5)
    )
    visit_two = BoardingVisitFactory.build(
        dog=dog, start_date=date(2021, 10, 6), end_date=date(2021, 10, 10)
    )
    visit_two.clean()


def test_dog_first_name_last_name_unique_together_fail():
    with pytest.raises(IntegrityError):
        DogFactory(first_name="Matt", last_name="Scott")
        DogFactory(first_name="Matt", last_name="Scott")


def test_dog_first_name_last_name_unique_together_ok():
    DogFactory(first_name="Matt", last_name="Scott")
    DogFactory(first_name="Matt", last_name="Gram")
