from django.contrib import admin
from django.utils.text import slugify

from Cosmetic_studio.product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'description',
        'image',
        'price',
        'units_sold',
        'slug',
        'user'
    )
    search_fields = (
        'name',
        'brand',
        'description',
        'user__email',
        'slug'
    )
    list_filter = ('brand', 'user',)
    fieldsets = (
        ('Product', {
            'fields': ('name', 'brand', 'image', 'price', 'units_sold','slug')
        }),
        ('Product details', {
            'fields': ('description',)
        }),
    )
    ordering = ('price', 'units_sold', '-created_at',)
    date_hierarchy = 'created_at'

    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(f'{obj.brand}-{obj.name}')
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)
