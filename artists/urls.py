from django.urls import path

from .views  import NewAritstsView

urlpatterns = [
    path('/new', NewAritstsView.as_view()),
]