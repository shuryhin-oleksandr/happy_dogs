import logging
from datetime import date, timedelta

from django.views.generic import TemplateView, ListView

from happy_dogs.dogs.models import Visit

logger = logging.getLogger(__name__)


# TODO: Move to utils
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class CalendarView(TemplateView):
    template_name = "dogs/calendar.html"

    def get_context_data(self, **kwargs):
        start_date = date(2021, 10, 1)
        end_date = date(2021, 10, 31)

        calendar_data = []
        for calendar_date in daterange(start_date, end_date):
            dogs_count = Visit.objects.filter(
                start_date__lte=calendar_date, end_date__gte=calendar_date
            ).count()
            calendar_record = {"date": calendar_date, "dogs_count": dogs_count}
            calendar_data.append(calendar_record)

        kwargs['calendar_data'] = calendar_data
        logger.info([record for record in calendar_data if record['dogs_count'] != 0])
        return super().get_context_data(**kwargs)


class DateVisitsListView(ListView):
    model = Visit
    template_name = "dogs/date_visits_list.html"

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
