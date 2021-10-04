from django.urls import path

from happy_dogs.dogs.views import CalendarView, DateVisitsListView

app_name = "dogs"
urlpatterns = [
    path("calendar/", CalendarView.as_view()),
    # TODO: Fix parsing
    path("calendar/<int:year>/<int:month>/<int:day>/", DateVisitsListView.as_view()),
]
