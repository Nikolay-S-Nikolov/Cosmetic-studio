from django.contrib import admin

from Cosmetic_studio.common.models import TeamMemberCard, IndexPageAds


@admin.register(TeamMemberCard)
class TeamMemberCardAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'role',
        'is_active',
        'appearance_order',
        'created_at',
        'updated_at',
    )
    list_filter = ('is_active', 'role')
    search_fields = ('name', 'role', 'description')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(IndexPageAds)
class IndexPageAdsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'adv_description')
    readonly_fields = ('created_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
