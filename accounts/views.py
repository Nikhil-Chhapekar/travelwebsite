from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile, WishlistItem
from .forms import UserProfileForm, CustomUserCreationForm
from destinations.models import Destination

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                # Redirect to the page the user was trying to access, or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Discovering Paradise.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """User profile view"""
    user_profile = request.user.profile

    # Get user's bookings
    bookings = request.user.bookings.order_by('-created_at')[:5]

    # Get user's reviews
    reviews = request.user.reviews.select_related('destination').order_by('-created_at')[:5]

    # Get user's wishlist
    wishlist_items = request.user.wishlist_items.select_related('destination').order_by('-added_at')[:5]

    context = {
        'profile': user_profile,
        'bookings': bookings,
        'reviews': reviews,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile view"""
    user_profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def wishlist(request):
    """User wishlist view"""
    wishlist_items = request.user.wishlist_items.select_related('destination').order_by('-added_at')
    return render(request, 'accounts/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, destination_slug):
    """Add destination to wishlist"""
    destination = get_object_or_404(Destination, slug=destination_slug)

    # Check if already in wishlist
    if not WishlistItem.objects.filter(user=request.user, destination=destination).exists():
        WishlistItem.objects.create(user=request.user, destination=destination)
        messages.success(request, f'{destination.name} has been added to your wishlist.')
    else:
        messages.info(request, f'{destination.name} is already in your wishlist.')

    # Redirect back to the destination page
    return redirect('destination_detail', slug=destination_slug)

@login_required
def remove_from_wishlist(request, item_id):
    """Remove destination from wishlist"""
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)
    destination_name = wishlist_item.destination.name
    wishlist_item.delete()
    messages.success(request, f'{destination_name} has been removed from your wishlist.')
    return redirect('wishlist')

def logout_view(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
