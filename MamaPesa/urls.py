"""
URL configuration for MamaPesa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from main.sitemap import ClassSitemap

sitemaps = {
    'static': ClassSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('vision/', include('vision.urls')),
    path('auth/', include('auth0.urls')),
    path('chat/', include('chatbot.urls')),
    #path('mpesa/', include('mpesa_api.urls')),
    path('google07949db9b98a31b8.html', TemplateView.as_view(template_name="main/google07949db9b98a31b8.html")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]