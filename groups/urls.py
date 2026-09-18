from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('create/', views.create_group_view, name='create_group'),
]