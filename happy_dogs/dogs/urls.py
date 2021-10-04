from django.urls import path

from happy_dogs.dogs.views import CalendarView

app_name = "dogs"
urlpatterns = [
    path("calendar/", CalendarView.as_view())
]
