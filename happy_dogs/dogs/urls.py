from django.urls import path

from happy_dogs.dogs.views import BoardingCalendarView, BoardingVisitsListView

app_name = "dogs"
urlpatterns = [
    path("boarding-calendar/", BoardingCalendarView.as_view(), name="boarding-calendar"),
    # TODO: Fix parsing
    path(
        "calendar/<int:year>/<int:month>/<int:day>/",
        BoardingVisitsListView.as_view(),
        name="boarding-visits",
    ),
]
