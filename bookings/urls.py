from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('create/<slug:destination_slug>/', views.create_booking, name='create_booking'),
    path('<uuid:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<uuid:booking_id>/payment/', views.booking_payment, name='booking_payment'),
    path('<uuid:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('<uuid:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('<uuid:booking_id>/confirm/', views.confirm_booking, name='confirm_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
