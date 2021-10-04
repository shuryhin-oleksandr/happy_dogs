import logging
from datetime import date, timedelta

from django.views.generic import TemplateView, ListView

from happy_dogs.dogs.forms import BoardingFilterForm
from happy_dogs.dogs.models import Visit

logger = logging.getLogger(__name__)


# TODO: Move to utils
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


class BoardingView(TemplateView):
    template_name = "dogs/boarding.html"
    form_class = BoardingFilterForm

    def get_context_data(self, **kwargs):
        if self.request.GET:
            filter_form = self.form_class(self.request.GET)
        else:
            filter_form = self.form_class({})
        form_is_valid = filter_form.is_valid()

        boarding_data = []
        if form_is_valid:
            start_date = filter_form.cleaned_data.get('start_date')
            end_date = filter_form.cleaned_data.get('end_date')

            for calendar_date in daterange(start_date, end_date):
                dogs_count = Visit.objects.filter(
                    start_date__lte=calendar_date, end_date__gte=calendar_date
                ).count()
                boarding_record = {"date": calendar_date, "dogs_count": dogs_count}
                boarding_data.append(boarding_record)

        kwargs['filter_form'] = filter_form
        kwargs['calendar_data'] = boarding_data
        return super().get_context_data(**kwargs)


class BoardingDayView(ListView):
    model = Visit
    template_name = "dogs/boarding_visits_list.html"

    def get_calendar_date(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        return date(year, month, day)

    def get_context_data(self, **kwargs):
        kwargs['error_message'] = None

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        try:
            calendar_date = self.get_calendar_date()
        except ValueError:
            return []

        visits = super().get_queryset()
        visits = visits.filter(start_date__lte=calendar_date, end_date__gte=calendar_date)
        return visits
