from django.contrib import admin

from .models import BusinessProfile, Service, TeamMember


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'status', 'owner', 'created_at')
    list_filter = ('status', 'city')
    search_fields = ('name', 'city', 'email')
    list_editable = ('status',)


admin.site.register(Service)
admin.site.register(TeamMember)
