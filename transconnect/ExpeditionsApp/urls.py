from django.urls import path

from .views import ListeViewExpedition, ExpeditionDetailView


app_name = "expeditions"


urlpatterns = [
    path(
        "",
        ListeViewExpedition.as_view(),
        name="liste"
    ),

    path(
        "<str:reference>/",
        ExpeditionDetailView.as_view(),
        name="detail"
    ),
]
