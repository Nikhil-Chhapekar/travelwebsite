from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Destination, Accommodation, Activity, AccommodationBooking
from .forms import AccommodationBookingForm
from reviews.models import Review

def destination_list(request):
    """View for listing all destinations"""
    destinations = Destination.objects.all()

    # Filter by continent if specified
    continent = request.GET.get('continent')
    if continent:
        destinations = destinations.filter(continent=continent)

    # Search functionality
    query = request.GET.get('q')
    if query:
        destinations = destinations.filter(
            name__icontains=query
        ) | destinations.filter(
            country__icontains=query
        ) | destinations.filter(
            description__icontains=query
        )

    # Sort functionality
    sort_order = request.GET.get('sort', 'asc')  # Default to ascending
    if sort_order == 'desc':
        destinations = destinations.order_by('-name')  # Descending order by name
    else:
        destinations = destinations.order_by('name')  # Ascending order by name

    # Pagination
    paginator = Paginator(destinations, 9)  # Show 9 destinations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'continent': continent,
        'query': query,
        'sort_order': sort_order,
    }
    return render(request, 'destinations/destination_list.html', context)

def destination_detail(request, slug):
    """View for showing destination details"""
    destination = get_object_or_404(Destination, slug=slug)

    # Get accommodations for this destination
    accommodations = destination.accommodations.all()

    # Get activities for this destination
    activities = destination.activities.all()

    # Get reviews for this destination
    reviews = destination.reviews.select_related('user').order_by('-created_at')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'destination': destination,
        'accommodations': accommodations,
        'activities': activities,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'destinations/destination_detail.html', context)

def destination_by_continent(request, continent):
    """View for listing destinations by continent"""
    destinations = Destination.objects.filter(continent=continent)

    # Get continent display name
    continent_name = dict(Destination.CONTINENT_CHOICES).get(continent, 'Unknown')

    # Sort functionality
    sort_order = request.GET.get('sort', 'asc')  # Default to ascending
    if sort_order == 'desc':
        destinations = destinations.order_by('-name')  # Descending order by name
    else:
        destinations = destinations.order_by('name')  # Ascending order by name

    # Pagination
    paginator = Paginator(destinations, 9)  # Show 9 destinations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'continent': continent,
        'continent_name': continent_name,
        'sort_order': sort_order,
    }
    return render(request, 'destinations/destination_list.html', context)

def destination_search(request):
    """View for searching destinations"""
    query = request.GET.get('q', '')

    if query:
        destinations = Destination.objects.filter(
            name__icontains=query
        ) | Destination.objects.filter(
            country__icontains=query
        ) | Destination.objects.filter(
            description__icontains=query
        )
    else:
        destinations = Destination.objects.none()

    # Pagination
    paginator = Paginator(destinations, 9)  # Show 9 destinations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'destinations/search_results.html', context)

def accommodation_detail(request, pk):
    """View for showing accommodation details and handling booking form"""
    accommodation = get_object_or_404(Accommodation, pk=pk)

    # Get reviews for this accommodation
    reviews = accommodation.reviews.select_related('user').order_by('-created_at')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Handle booking form submission
    if request.method == 'POST':
        from .forms import AccommodationBookingForm
        form = AccommodationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.accommodation = accommodation
            booking.save()

            # Add success message
            from django.contrib import messages
            messages.success(request, 'Your booking request has been submitted successfully! We will contact you shortly to confirm your reservation.')

            # Redirect to the same page to avoid form resubmission
            return redirect('accommodation_detail', pk=pk)
    else:
        from .forms import AccommodationBookingForm
        form = AccommodationBookingForm()

    context = {
        'accommodation': accommodation,
        'destination': accommodation.destination,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
    }
    return render(request, 'destinations/accommodation_detail.html', context)

def activity_detail(request, pk):
    """View for showing activity details"""
    activity = get_object_or_404(Activity, pk=pk)

    # Get reviews for this activity
    reviews = activity.reviews.select_related('user').order_by('-created_at')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'activity': activity,
        'destination': activity.destination,
        'reviews': reviews,
        'avg_rating': avg_rating,
    }
    return render(request, 'destinations/activity_detail.html', context)
