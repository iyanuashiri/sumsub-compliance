from django.urls import path

from rest_framework.schemas import get_schema_view

from . import views

schema_view = get_schema_view(title='Compliances API')

app_name = 'compliances'
urlpatterns = [
    path('documents/', views.DocumentCreateView.as_view()),
    path('appliants/', views.ApplicantCreateView.as_view()),


]
