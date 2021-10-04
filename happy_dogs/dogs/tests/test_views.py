from datetime import date

import pytest
from django.urls import reverse
from pytest_factoryboy import register

from happy_dogs.dogs.factories import BoardingVisitFactory

register(BoardingVisitFactory)
pytestmark = pytest.mark.django_db


def test_boarding_view(client):
    url = reverse("dogs:boarding")
    BoardingVisitFactory(start_date=date(2021, 10, 1), end_date=date(2021, 10, 5))
    filter_data = {"start_date": date(2021, 10, 1), "end_date": date(2021, 10, 10)}

    response = client.get(url, data=filter_data)
    boarding_data = response.context_data.get("boarding_data")
    filled_boarding_record = [
        boarding_record
        for boarding_record in boarding_data
        if boarding_record["date"] == date(2021, 10, 3)
    ][0]
    empty_boarding_record = [
        boarding_record
        for boarding_record in boarding_data
        if boarding_record["date"] == date(2021, 10, 7)
    ][0]

    assert response.status_code == 200
    assert filled_boarding_record.get("dogs_count") == 1
    assert empty_boarding_record.get("dogs_count") == 0


def test_boarding_view_no_filter_data(client):
    url = reverse("dogs:boarding")
    BoardingVisitFactory(start_date=date(2021, 10, 1), end_date=date(2021, 10, 5))

    response = client.get(url)
    boarding_data = response.context_data.get("boarding_data")
    assert response.status_code == 200
    assert len(boarding_data) == 31


def test_boarding_view_no_filter_start_date(client):
    url = reverse("dogs:boarding")
    filter_data = {"end_date": date(2021, 10, 10)}

    response = client.get(url, filter_data)
    boarding_data = response.context_data.get("boarding_data")
    boarding_data_records_dates = [
        boarding_record.get("date") for boarding_record in boarding_data
    ]
    boarding_data_max_date = max(boarding_data_records_dates)

    assert response.status_code == 200
    assert boarding_data_max_date == date(2021, 10, 10)


def test_boarding_view_no_filter_end_date(client):
    url = reverse("dogs:boarding")
    filter_data = {"start_date": date(2021, 10, 20)}

    response = client.get(url, filter_data)
    boarding_data = response.context_data.get("boarding_data")
    boarding_data_records_dates = [
        boarding_record.get("date") for boarding_record in boarding_data
    ]
    boarding_data_min_date = min(boarding_data_records_dates)

    assert response.status_code == 200
    assert boarding_data_min_date == date(2021, 10, 20)
