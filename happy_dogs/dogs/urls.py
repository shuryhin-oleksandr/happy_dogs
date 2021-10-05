from django.urls import path

from happy_dogs.dogs.views import BoardingView, BoardingDayView, DogCreateView, \
    BoardingVisitCreateView, CreateBoardingTestDataView, BoardingAPIView, BoardingDayAPIView

app_name = "dogs"
urlpatterns = [
    path("boarding/", BoardingView.as_view(), name="boarding"),
    # TODO: Fix parsing
    path(
        "boarding/<int:year>/<int:month>/<int:day>/",
        BoardingDayView.as_view(),
        name="boarding-day",
    ),
    path("add-dog/", DogCreateView.as_view(), name="add-dog"),
    path("add-visit/", BoardingVisitCreateView.as_view(), name="add-visit"),
    path("create-boarding-test-data/", CreateBoardingTestDataView.as_view(),
         name="create-boarding-test-data"),

    path("boarding-api/", BoardingAPIView.as_view(), name="boarding-api"),
    path(
        "boarding-api/<int:year>/<int:month>/<int:day>/",
        BoardingDayAPIView.as_view(),
        name="boarding-day-api",
    ),

]
