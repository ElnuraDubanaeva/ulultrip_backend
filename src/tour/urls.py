from django.urls import path, include
from rest_framework import routers

from src.profiles.views import FavoriteTourApiView
from .views import (
    RegionListAPIView,
    ReviewViewSet,
    TourDetailView,
    GetSlugTitleListAPIView,
    TourListAPIView,
    GuideListAPIView,
    CategoryListAPIView,
    TourReviewsListAPIView,
    AboutUsListAPIView,
)

router = routers.SimpleRouter()
router.register(r"review", ReviewViewSet, basename="review")
router.register(r"tour", TourDetailView, basename="tour")

urlpatterns = [
    path("", include(router.urls)),
    path("slugs/", GetSlugTitleListAPIView.as_view(), name="slugs"),
    path("tours/", TourListAPIView.as_view(), name="tour_list"),
    path("guides/", GuideListAPIView.as_view(), name="guides"),
    path("regions/", RegionListAPIView.as_view(), name="regions"),
    path("categories/", CategoryListAPIView.as_view(), name="categories"),
    path(
        "tours/<str:slug>/favorite/",
        FavoriteTourApiView.as_view(),
        name="favorites-crud",
    ),
    path("tours/<slug:slug>/reviews/", TourReviewsListAPIView.as_view()),
    path("about_us/", AboutUsListAPIView.as_view()),
]
