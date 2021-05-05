"""younggulart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from arts.home_views import BannerView, NavView
from arts.views import ArtList
from orders.views import FrameView

urlpatterns = [
    path('nav', NavView.as_view()),
    path('banners', BannerView.as_view()),
    path('users', include('users.urls')),
    path('auctions', include('bids.auction_urls')),
    path('arts', include('arts.urls')),
    path('artlist/<int:media_id>', ArtList.as_view()),
    path('biddings', include('bids.bidding_urls')),
    path('frame/<int:art_id>', FrameView.as_view()),
]
