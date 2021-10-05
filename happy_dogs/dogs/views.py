import calendar
import logging
from datetime import date, timedelta
import random

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from happy_dogs.dogs.factories import DogFactory, BoardingVisitFactory
from happy_dogs.dogs.forms import BoardingFilterForm
from happy_dogs.dogs.models import BoardingVisit, Dog
from happy_dogs.dogs.serializers import BoardingVisitSerializer

logger = logging.getLogger(__name__)


# TODO: Move to utils
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


class BoardingView(TemplateView):
    template_name = "dogs/boarding.html"
    filter_form_class = BoardingFilterForm

    def get_context_data(self, **kwargs):
        today = date.today()
        last_month_day = calendar.monthrange(today.year, today.month)[1]
        start_date = self.request.GET.get('start_date') or today.replace(day=1)
        end_date = self.request.GET.get('end_date') or today.replace(day=last_month_day)

        filter_data = {
            'start_date': start_date,
            'end_date': end_date,
        }
        logger.info(filter_data)
        filter_form = self.filter_form_class(filter_data)

        boarding_data = []
        if filter_form.is_valid():
            start_date = filter_form.cleaned_data.get('start_date')
            end_date = filter_form.cleaned_data.get('end_date')

            for calendar_date in daterange(start_date, end_date):
                dogs_count = BoardingVisit.objects.filter(
                    start_date__lte=calendar_date, end_date__gte=calendar_date
                ).count()
                boarding_record = {"date": calendar_date, "dogs_count": dogs_count}
                boarding_data.append(boarding_record)

        kwargs['filter_form'] = filter_form
        kwargs['boarding_data'] = boarding_data
        return super().get_context_data(**kwargs)


class BoardingDayView(ListView):
    model = BoardingVisit
    template_name = "dogs/boarding-day.html"

    def get_calendar_date(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        return date(year, month, day)

    def get_context_data(self, **kwargs):
        try:
            self.get_calendar_date()
        except ValueError:
            kwargs['error_message'] = 'Invalid date format'
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        try:
            calendar_date = self.get_calendar_date()
        except ValueError:
            return []

        visits = super().get_queryset()
        visits = visits.filter(start_date__lte=calendar_date, end_date__gte=calendar_date)
        return visits


class DogCreateView(CreateView):
    model = Dog
    fields = ['first_name', 'last_name']
    template_name = 'dogs/create_dog.html'

    def get_success_url(self):
        return reverse_lazy('dogs:boarding')


class BoardingVisitCreateView(CreateView):
    model = BoardingVisit
    fields = ['dog', 'start_date', 'end_date']
    template_name = 'dogs/create_visit.html'

    def get_success_url(self):
        return reverse_lazy('dogs:boarding')


class CreateBoardingTestDataView(ListView):
    def get(self, request):
        Dog.objects.all().delete()
        BoardingVisit.objects.all().delete()

        TEST_DATA_YEAR = 2021
        dogs = [DogFactory() for i in range(10)]
        for month in range(1, 12):
            for dog in dogs:
                start_date = date(year=TEST_DATA_YEAR, month=month, day=random.randrange(1, 23))
                days_delta = random.randrange(1, 5)
                end_date = start_date + timedelta(days=days_delta)
                BoardingVisitFactory(start_date=start_date, end_date=end_date, dog=dog)

        return redirect('dogs:boarding')


class BoardingAPIView(APIView):
    filter_form_class = BoardingFilterForm

    def get(self, request):
        today = date.today()
        last_month_day = calendar.monthrange(today.year, today.month)[1]
        start_date = self.request.GET.get('start_date') or today.replace(day=1)
        end_date = self.request.GET.get('end_date') or today.replace(day=last_month_day)

        filter_data = {
            'start_date': start_date,
            'end_date': end_date,
        }
        logger.info(filter_data)
        filter_form = self.filter_form_class(filter_data)

        boarding_data = []
        if filter_form.is_valid():
            start_date = filter_form.cleaned_data.get('start_date')
            end_date = filter_form.cleaned_data.get('end_date')

            for calendar_date in daterange(start_date, end_date):
                dogs_count = BoardingVisit.objects.filter(
                    start_date__lte=calendar_date, end_date__gte=calendar_date
                ).count()
                boarding_record = {"date": calendar_date, "dogs_count": dogs_count}
                boarding_data.append(boarding_record)

        return Response(boarding_data)


class BoardingDayAPIView(ListAPIView):
    serializer_class = BoardingVisitSerializer

    def get_calendar_date(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        return date(year, month, day)

    def get_queryset(self):
        try:
            calendar_date = self.get_calendar_date()
        except ValueError:
            raise ValidationError("Invalid input date format")

        visits = BoardingVisit.objects.filter(start_date__lte=calendar_date,
                                              end_date__gte=calendar_date)
        return visits
