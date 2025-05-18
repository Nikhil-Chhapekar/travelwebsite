from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid

class Destination(models.Model):
    CONTINENT_CHOICES = [
        ('AF', 'Africa'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('SA', 'South America'),
        ('OC', 'Oceania'),
        ('AN', 'Antarctica'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    country = models.CharField(max_length=100)
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES)
    description = models.TextField()
    highlights = models.TextField()
    best_time_to_visit = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destinations/')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.country}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'slug': self.slug})

    def average_rating(self):
        """Calculate the average rating for this destination"""
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg or 4.5  # Default to 4.5 if no reviews

    class Meta:
        ordering = ['name']

class Accommodation(models.Model):
    TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('hostel', 'Hostel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('guesthouse', 'Guesthouse'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accommodations/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.destination.name}"

    def average_rating(self):
        """Calculate the average rating for this accommodation"""
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg or 4.5  # Default to 4.5 if no reviews

class Activity(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

    def average_rating(self):
        """Calculate the average rating for this activity"""
        from django.db.models import Avg
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return avg or 4.5  # Default to 4.5 if no reviews

    class Meta:
        verbose_name_plural = 'Activities'

class AccommodationBooking(models.Model):
    ROOM_TYPE_CHOICES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
    ]

    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='accommodation_bookings')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.accommodation.name} ({self.check_in_date} to {self.check_out_date})"

    class Meta:
        ordering = ['-created_at']
