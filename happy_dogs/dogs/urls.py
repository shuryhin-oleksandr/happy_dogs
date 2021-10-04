from django.urls import path

from happy_dogs.dogs.views import BoardingView, BoardingDayView

app_name = "dogs"
urlpatterns = [
    path("boarding/", BoardingView.as_view(), name="boarding"),
    # TODO: Fix parsing
    path(
        "boarding/<int:year>/<int:month>/<int:day>/",
        BoardingDayView.as_view(),
        name="boarding-day",
    ),
]
