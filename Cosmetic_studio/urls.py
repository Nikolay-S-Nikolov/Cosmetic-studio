"""
URL configuration for Cosmetic_studio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Cosmetic_studio.common.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Cosmetic_studio.common.urls")),
    path('accounts/', include('Cosmetic_studio.accounts.urls')),
    path('services/', include('Cosmetic_studio.services.urls')),
    path('shop/', include('Cosmetic_studio.product.urls')),
    path('orders/', include('Cosmetic_studio.orders.urls')),
    path('blog/', include('Cosmetic_studio.blog.urls')),
    path('contact/', include('Cosmetic_studio.contact.urls')),
    path('health/', health_check, name='health_check'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
