import logging
from datetime import date, timedelta

from django.views.generic import TemplateView, ListView

from happy_dogs.dogs.forms import BoardingCalendarFilterForm
from happy_dogs.dogs.models import Visit

logger = logging.getLogger(__name__)


# TODO: Move to utils
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


class BoardingView(TemplateView):
    template_name = "dogs/boarding_calendar.html"
    filter_form_class = BoardingCalendarFilterForm

    def get_context_data(self, **kwargs):
        filter_form = self.filter_form_class(self.request.GET)

        calendar_data = []
        if filter_form.is_valid():
            start_date = filter_form.cleaned_data.get('start_date')
            end_date = filter_form.cleaned_data.get('end_date')

            for calendar_date in daterange(start_date, end_date):
                dogs_count = Visit.objects.filter(
                    start_date__lte=calendar_date, end_date__gte=calendar_date
                ).count()
                calendar_record = {"date": calendar_date, "dogs_count": dogs_count}
                calendar_data.append(calendar_record)

        kwargs['filter_form'] = filter_form
        kwargs['calendar_data'] = calendar_data
        return super().get_context_data(**kwargs)


class BoardingDayView(ListView):
    model = Visit
    template_name = "dogs/boarding_visits_list.html"

    # TODO: use filters
    def get_queryset(self):
        # TODO: Add validation
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        calendar_date = date(year, month, day)

        visits = super().get_queryset()
        visits = visits.filter(start_date__lte=calendar_date, end_date__gte=calendar_date)
        return visits
