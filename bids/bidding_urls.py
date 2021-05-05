from django.urls import path

from .views import BiddingView

urlpatterns = [
    path('/<int:art_id>', BiddingView.as_view()),
    path('/in-progress', BiddingView.as_view()),
]