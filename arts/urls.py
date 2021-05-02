from django.urls import path

from .arts_views  import ArtDetailView

urlpatterns = [
    path('/<int:art_id>', ArtDetailView.as_view()),
]
