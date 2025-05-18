from django.contrib import admin
from .models import Destination, Accommodation, Activity, AccommodationBooking

class AccommodationInline(admin.TabularInline):
    model = Accommodation
    extra = 1

class ActivityInline(admin.TabularInline):
    model = Activity
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'continent', 'featured', 'created_at')
    list_filter = ('continent', 'featured', 'created_at')
    search_fields = ('name', 'country', 'description')
    prepopulated_fields = {'slug': ('name', 'country')}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AccommodationInline, ActivityInline]
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'country', 'continent', 'image', 'featured')
        }),
        ('Detailed Information', {
            'fields': ('description', 'highlights', 'best_time_to_visit')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def make_featured(self, request, queryset):
        queryset.update(featured=True)
    make_featured.short_description = "Mark selected destinations as featured"

    def remove_featured(self, request, queryset):
        queryset.update(featured=False)
    remove_featured.short_description = "Remove selected destinations from featured"

    actions = ['make_featured', 'remove_featured']

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'type', 'price_per_night')
    list_filter = ('type', 'destination__continent')
    search_fields = ('name', 'description', 'destination__name')
    list_per_page = 20

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'duration', 'price')
    list_filter = ('destination__continent',)
    search_fields = ('name', 'description', 'destination__name')
    list_per_page = 20

@admin.register(AccommodationBooking)
class AccommodationBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'accommodation', 'full_name', 'email', 'check_in_date', 'check_out_date', 'room_type', 'guests', 'created_at')
    list_filter = ('room_type', 'check_in_date', 'check_out_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'accommodation__name')
    readonly_fields = ('booking_id', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'accommodation', 'created_at')
        }),
        ('Guest Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Stay Details', {
            'fields': ('check_in_date', 'check_out_date', 'room_type', 'guests', 'special_requests')
        }),
    )
