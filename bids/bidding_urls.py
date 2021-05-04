from django.urls import path

from .views import BiddingView

urlpatterns = [
    path('/in-progress', BiddingView.as_view()),
]