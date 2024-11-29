from django.contrib import admin

from Cosmetic_studio.contact.models import ContactInfo


# Register your models here.
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'address', 'custom_message', 'working_time', 'created_at', 'visible')
    search_fields = ('phone_number', 'address', 'custom_message', 'working_time')
    list_filter = ('visible', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'address', 'custom_message', 'working_time', 'visible')
        }),
        ('Additional Information', {
            'fields': ('created_at',)
        }),
    )
    actions = ['make_visible', 'make_invisible']

    def make_visible(self, request, queryset):
        queryset.update(visible=True)
        self.message_user(request, "Successfully made selected contact information visible.")

    make_visible.short_description = "Make selected contact information visible"

    def make_invisible(self, request, queryset):
        queryset.update(visible=False)
        self.message_user(request, "Successfully made selected contact information invisible.")

    make_invisible.short_description = "Make selected contact information invisible"

