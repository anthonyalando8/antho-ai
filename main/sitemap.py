# myapp/sitemap.py

from django.contrib import sitemaps
from django.urls import reverse

class ClassSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['auth0:login', 'chatbot:chat', 'main:airtime', 'auth0:register']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        if item in ['auth0:login', 'chatbot:chat']:
            return 1.0
        else:
            return 0.8
