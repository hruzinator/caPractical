from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^postReview/', views.postReview, name="postReview"),
    url(r'^getReview/',views.getReview, name="getReview")
]
