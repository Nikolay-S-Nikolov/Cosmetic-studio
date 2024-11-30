from django.shortcuts import render
from django.views import generic as views

from Cosmetic_studio.blog.models import BlogContent, Tag
from Cosmetic_studio.product.models import Product


class DetailsProductView(views.DetailView):
    model = Product
    template_name = "products/details_product.html"


class ListProductsView(views.ListView):
    model = Product
    template_name = "products/list_products.html"
    paginate_by = 8
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['random_list'] = BlogContent.objects.order_by('?')[:4]
        context['tags_list'] = Tag.objects.order_by('name')
        return context
