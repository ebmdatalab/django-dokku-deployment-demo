from django.urls import path

from d4.views import index


urlpatterns = [
    path("", index, name="index"),
]
