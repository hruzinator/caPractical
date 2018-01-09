from django.urls import path

from . import views

urlpatterns = [
    path('postReview/', views.postReview, name="postReview"),
    path('getReview/<int:reviewId>/',views.getReview, name="getReview"),
    path('getOwnReviews/', views.getOwnReviews, name="getOwnReviews")
]
