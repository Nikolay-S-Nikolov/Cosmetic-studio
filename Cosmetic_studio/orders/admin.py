from django.contrib import admin
from django.db.models import Sum
from django.urls import reverse
from django.utils.html import format_html

from Cosmetic_studio.orders.models import Order, OrderItem, ShippingAddress


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price', 'subtotal')
    fields = (
        'product',
        'quantity',
        'price',
        'subtotal',
    )

    def subtotal(self, instance):
        if instance.quantity is None or instance.price is None:
            return 0
        return int(instance.quantity) * float(instance.price)

    subtotal.short_description = 'Subtotal'


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0
    readonly_fields = ('created_at', 'customer')
    fieldsets = (
        ('Customer Info', {'fields': ('customer', 'name', 'phone_number', 'email')}),
        ('Address', {'fields': ('address', 'city', 'postal_code')}),
        ('Payment', {'fields': ('payment_method',)}),
        ('Other', {'fields': ('created_at',)}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'status',
        'created_at',
        'updated_at',
        'total_price',
        'customer_link',
        'items_count',
    )

    list_display_links = ('pk', 'status',)

    search_fields = (
        'pk',
        'customer__email',
        'status',
        'shippingaddress__phone_number'
    )

    list_filter = ('status', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = (
        'created_at',
        'updated_at',
        'customer',
        'total_price',
        'items_count'
    )

    actions = ['order_processing', 'order_completed', 'order_cancelled']

    inlines = [OrderItemInline, ShippingAddressInline]

    fieldsets = (
        ('Order Info', {'fields': ('status', 'customer', 'total_price', 'items_count')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )

    def customer_link(self, obj):
        url = reverse('admin:accounts_studiouser_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', url, obj.customer.email)

    customer_link.short_description = 'Customer'

    def items_count(self, obj):
        return obj.items.count()

    items_count.short_description = 'Number of Items'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _items_count=Sum('items__quantity')
        )
        return queryset

    def order_processing(self, request, queryset):
        updated = queryset.update(status='Processing')
        self.message_user(
            request,
            f"{updated} orders were successfully marked as Processing.",
        )

    order_processing.short_description = "Mark selected order as Processing"

    def order_completed(self, request, queryset):
        updated = queryset.update(status='Completed')
        self.message_user(request, f"{updated} orders were successfully marked as Completed.")

    order_completed.short_description = "Mark selected orders as Completed"

    def order_cancelled(self, request, queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f"{updated} orders were successfully marked as Cancelled.")

    order_cancelled.short_description = "Mark selected orders as Cancelled"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order_link',
        'product_link',
        'quantity',
        'price',
        'subtotal'
    )

    search_fields = ('order__pk', 'product__name')
    list_filter = ('order__status', 'product')
    readonly_fields = ('subtotal',)

    def order_link(self, obj):
        url = reverse("admin:orders_order_change", args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.pk)

    order_link.short_description = 'Order'

    def product_link(self, obj):
        url = reverse("admin:product_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)

    product_link.short_description = 'Product'

    def subtotal(self, obj):
        return obj.quantity * obj.price

    subtotal.short_description = 'Subtotal'


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):

    list_display = (
        'created_at',
        'order_link',
        'customer_link',
        'phone_number',
        'email',
        'city',
        'payment_method',
    )

    list_display_links = (
        'order_link',
        'customer_link',
        'created_at'
    )

    search_fields = (
        'order__id',
        'customer__email',
        'phone_number',
        'city',
    )

    list_filter = (
        'city',
        'payment_method',
        'created_at',
    )

    date_hierarchy = 'created_at'

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'customer',
        'order',
    )

    fieldsets = (
        ('Order Info', {'fields': ('order', 'customer')}),
        ('Contact Info', {'fields': ('name', 'phone_number', 'email')}),
        ('Address', {'fields': ('address', 'city', 'postal_code')}),
        ('Payment', {'fields': ('payment_method',)}),
        ('Other', {'fields': ('created_at',)}),
    )

    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.pk)

    order_link.short_description = 'Order'

    def customer_link(self, obj):
        url = reverse('admin:accounts_studiouser_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', url, obj.customer.email)

    customer_link.short_description = 'Customer'
