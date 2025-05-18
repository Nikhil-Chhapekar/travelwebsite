from django.contrib import admin
from .models import Booking, BookingActivity, Payment

class BookingActivityInline(admin.TabularInline):
    model = BookingActivity
    extra = 0
    readonly_fields = ('price',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_id', 'created_at')
    can_delete = False

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'destination', 'start_date', 'end_date', 'status', 'total_price')
    list_filter = ('status', 'start_date', 'destination__continent')
    search_fields = ('booking_id', 'user__username', 'user__email', 'destination__name')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    inlines = [BookingActivityInline, PaymentInline]
    list_per_page = 20

    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'destination', 'accommodation')
        }),
        ('Dates and Guests', {
            'fields': ('start_date', 'end_date', 'adults', 'children')
        }),
        ('Status and Price', {
            'fields': ('status', 'total_price', 'special_requests')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected bookings as completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"

    actions = ['mark_as_confirmed', 'mark_as_completed', 'mark_as_cancelled']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'booking__booking_id', 'booking__user__username')
    readonly_fields = ('payment_id', 'created_at')
    list_per_page = 20

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        # Also update the related booking status
        for payment in queryset:
            payment.booking.status = 'confirmed'
            payment.booking.save()
    mark_as_completed.short_description = "Mark selected payments as completed"

    def mark_as_refunded(self, request, queryset):
        queryset.update(status='refunded')
        # Also update the related booking status
        for payment in queryset:
            payment.booking.status = 'cancelled'
            payment.booking.save()
    mark_as_refunded.short_description = "Mark selected payments as refunded"

    actions = ['mark_as_completed', 'mark_as_refunded']
