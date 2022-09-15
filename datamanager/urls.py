from django.urls import path
from datamanager import views

urlpatterns = [
    path("top10citacoes/", views.Top10CitacoesAPI.as_view()),
]