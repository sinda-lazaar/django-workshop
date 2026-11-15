
from django.contrib import admin
from django.urls import include, path

from .views import index, homeWithName


urlpatterns = [

    path("", index, name="homepage"),

    path("home/<str:nom>/", homeWithName, name="home"),

    path("admin/", admin.site.urls),

    path(
        "expeditions/",
        include("ExpeditionsApp.urls")
    ),

    path(
        "vehicules/",
        include("VehiculesApp.urls")
    ),

    path(
        "entreprises/",
        include("EntreprisesApp.urls")
    ),

    path(
        "offres/",
        include("OffresApp.urls")
    ),
]
