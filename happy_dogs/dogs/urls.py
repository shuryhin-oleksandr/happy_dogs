from django.urls import path

from happy_dogs.dogs.views import BoardingView, BoardingDayView, DogCreateView, \
    BoardingVisitCreateView

app_name = "dogs"
urlpatterns = [
    path("boarding/", BoardingView.as_view(), name="boarding"),
    # TODO: Fix parsing
    path(
        "boarding/<int:year>/<int:month>/<int:day>/",
        BoardingDayView.as_view(),
        name="boarding-day",
    ),
    path("add-dog", DogCreateView.as_view(), name="add-dog"),
    path("add-visit", BoardingVisitCreateView.as_view(), name="add-visit"),
]
