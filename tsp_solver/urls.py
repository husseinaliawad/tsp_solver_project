from django.urls import path
from .views import tsp_solver

urlpatterns = [
    path('', tsp_solver, name='tsp_solver'),
]
