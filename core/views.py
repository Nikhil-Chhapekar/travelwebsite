from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from destinations.models import Destination
from reviews.models import Review
from .models import ContactMessage, Newsletter, FAQ
from .forms import ContactForm, NewsletterForm

def home(request):
    """Home page view"""
    # Get featured destinations
    featured_destinations = Destination.objects.filter(featured=True)[:6]

    # Get recent reviews
    recent_reviews = Review.objects.select_related('user', 'destination').order_by('-created_at')[:3]

    # Newsletter form
    newsletter_form = NewsletterForm()

    context = {
        'featured_destinations': featured_destinations,
        'recent_reviews': recent_reviews,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'core/about.html')

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

def faq(request):
    """FAQ page view"""
    faqs = FAQ.objects.all()
    return render(request, 'core/faq.html', {'faqs': faqs})

def newsletter_subscribe(request):
    """Newsletter subscription view"""
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Check if already subscribed
            if Newsletter.objects.filter(email=email).exists():
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'info', 'message': 'You are already subscribed to our newsletter.'})
                messages.info(request, 'You are already subscribed to our newsletter.')
            else:
                form.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'success', 'message': 'Thank you for subscribing to our newsletter!'})
                messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please enter a valid email address.'})
            messages.error(request, 'Please enter a valid email address.')

    # If not AJAX or not POST, redirect to home
    return redirect('home')

def privacy_policy(request):
    """Privacy policy page view"""
    return render(request, 'core/privacy_policy.html')

def terms(request):
    """Terms of service page view"""
    return render(request, 'core/terms.html')

def sitemap(request):
    """Sitemap page view"""
    return render(request, 'core/sitemap.html')
