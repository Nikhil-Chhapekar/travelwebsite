from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Booking, BookingActivity, Payment
from .forms import BookingForm, PaymentForm
from destinations.models import Destination, Accommodation, Activity

def booking_list(request):
    """View for listing all bookings (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    # Get filter parameters
    status = request.GET.get('status')
    destination_id = request.GET.get('destination')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    # Start with all bookings
    bookings = Booking.objects.select_related('user', 'destination', 'accommodation').all()

    # Apply filters
    if status:
        bookings = bookings.filter(status=status)
    if destination_id:
        bookings = bookings.filter(destination_id=destination_id)
    if date_from:
        bookings = bookings.filter(start_date__gte=date_from)
    if date_to:
        bookings = bookings.filter(end_date__lte=date_to)

    # Get all destinations for the filter dropdown
    destinations = Destination.objects.all()

    context = {
        'bookings': bookings,
        'destinations': destinations,
    }
    return render(request, 'bookings/booking_list.html', context)

@login_required
def my_bookings(request):
    """View for listing user's bookings"""
    bookings = Booking.objects.select_related('destination', 'accommodation').filter(user=request.user)
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    """View for showing booking details"""
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # Check if the user is the owner of the booking or staff
    if booking.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to view this booking.")

    # Get booking activities
    activities = booking.booking_activities.select_related('activity').all()

    # Get payment information
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        payment = None

    context = {
        'booking': booking,
        'activities': activities,
        'payment': payment,
    }
    return render(request, 'bookings/booking_detail.html', context)

@login_required
def create_booking(request, destination_slug):
    """View for creating a new booking"""
    destination = get_object_or_404(Destination, slug=destination_slug)

    if request.method == 'POST':
        form = BookingForm(request.POST, destination=destination)
        if form.is_valid():
            # Create booking but don't save yet
            booking = form.save(commit=False)
            booking.user = request.user
            booking.destination = destination

            # Calculate total price
            accommodation = form.cleaned_data['accommodation']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']

            # Calculate number of nights
            nights = (end_date - start_date).days

            # Base price is accommodation price * nights * number of people
            total_price = accommodation.price_per_night * nights * (adults + (children * Decimal('0.5')))

            # Add selected activities to the total price
            selected_activities = form.cleaned_data.get('activities', [])

            booking.total_price = total_price
            booking.save()

            # Create booking activities
            for activity in selected_activities:
                activity_date = start_date + timedelta(days=1)  # Default to second day
                participants = adults + children
                activity_price = activity.price * participants

                BookingActivity.objects.create(
                    booking=booking,
                    activity=activity,
                    date=activity_date,
                    participants=participants,
                    price=activity_price
                )

                # Add activity price to total
                total_price += activity_price

            # Update total price
            booking.total_price = total_price
            booking.save()

            messages.success(request, 'Your booking has been created. Please proceed to payment.')
            return redirect('booking_payment', booking_id=booking.booking_id)
    else:
        form = BookingForm(destination=destination)

    context = {
        'form': form,
        'destination': destination,
    }
    return render(request, 'bookings/create_booking.html', context)

@login_required
def booking_payment(request, booking_id):
    """View for processing booking payment"""
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # Check if the user is the owner of the booking
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to pay for this booking.")

    # Check if payment already exists
    try:
        payment = booking.payment
        if payment.status == 'completed':
            messages.info(request, 'This booking has already been paid for.')
            return redirect('booking_confirmation', booking_id=booking.booking_id)
    except Payment.DoesNotExist:
        payment = None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Create payment
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_price
            payment.status = 'completed'  # In a real app, this would be handled by a payment gateway
            payment.transaction_id = f"TR-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            payment.save()

            # Update booking status
            booking.status = 'confirmed'
            booking.save()

            messages.success(request, 'Payment successful! Your booking has been confirmed.')
            return redirect('booking_confirmation', booking_id=booking.booking_id)
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'bookings/booking_payment.html', context)

@login_required
def booking_confirmation(request, booking_id):
    """View for showing booking confirmation"""
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # Check if the user is the owner of the booking
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to view this booking confirmation.")

    # Get booking activities
    activities = booking.booking_activities.select_related('activity').all()

    # Get payment information
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        payment = None

    context = {
        'booking': booking,
        'activities': activities,
        'payment': payment,
    }
    return render(request, 'bookings/booking_confirmation.html', context)

@login_required
def cancel_booking(request, booking_id):
    """View for cancelling a booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # Check if the user is the owner of the booking
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to cancel this booking.")

    # Check if booking can be cancelled
    if booking.status == 'completed':
        messages.error(request, 'Completed bookings cannot be cancelled.')
        return redirect('booking_detail', booking_id=booking.booking_id)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()

        # Update payment status if exists
        try:
            payment = booking.payment
            payment.status = 'refunded'
            payment.save()
        except Payment.DoesNotExist:
            pass

        messages.success(request, 'Your booking has been cancelled successfully.')
        return redirect('my_bookings')

    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

@login_required
def confirm_booking(request, booking_id):
    """View for admin to confirm a booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id)

    # Check if the user is staff
    if not request.user.is_staff:
        return HttpResponseForbidden("You don't have permission to confirm this booking.")

    # Check if booking can be confirmed
    if booking.status != 'pending':
        messages.error(request, 'Only pending bookings can be confirmed.')
        return redirect('booking_detail', booking_id=booking.booking_id)

    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()

        messages.success(request, f'Booking {booking.booking_id} has been confirmed successfully.')
        return redirect('booking_list')

    return redirect('booking_detail', booking_id=booking.booking_id)
