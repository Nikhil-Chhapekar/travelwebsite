from django.urls import path
from . import views

urlpatterns = [
    path('', views.destination_list, name='destination_list'),
    path('search/', views.destination_search, name='destination_search'),
    path('continent/<str:continent>/', views.destination_by_continent, name='destination_by_continent'),
    path('accommodation/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('<slug:slug>/', views.destination_detail, name='destination_detail'),
]
