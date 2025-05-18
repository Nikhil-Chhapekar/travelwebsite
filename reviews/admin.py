from django.contrib import admin
from .models import Review, AccommodationReview, ActivityReview

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'title', 'rating', 'visit_date', 'created_at')
    list_filter = ('rating', 'visit_date', 'created_at', 'destination__continent')
    search_fields = ('title', 'content', 'user__username', 'destination__name')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

@admin.register(AccommodationReview)
class AccommodationReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'accommodation', 'title', 'rating', 'stay_date', 'created_at')
    list_filter = ('rating', 'stay_date', 'created_at', 'accommodation__destination__continent')
    search_fields = ('title', 'content', 'user__username', 'accommodation__name')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(ActivityReview)
class ActivityReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'title', 'rating', 'activity_date', 'created_at')
    list_filter = ('rating', 'activity_date', 'created_at', 'activity__destination__continent')
    search_fields = ('title', 'content', 'user__username', 'activity__name')
    readonly_fields = ('created_at',)
    list_per_page = 20
