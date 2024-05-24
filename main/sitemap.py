# myapp/sitemap.py

from django.contrib import sitemaps
from django.urls import reverse

class ClassSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        # Return a list of dictionaries containing the URL names and additional attributes
        return [
            {'name': 'auth0:login', 'publication_name': 'SoftConnect | Sign In', 'publication_date': '2024-04-15', 'tags': 'authentication, login, Sign In, account','title': 'Sign In' },
            {'name': 'chatbot:chat', 'publication_name': 'SoftChatAI', 'publication_date': '2024-04-15', 'tags': 'chat, messaging, SoftChatAI, Gemini, GPT, AI', 'title': 'SoftChatAI'},
            #{'name': 'main:airtime', 'publication_name': 'SoftConnect | By airtime', 'publication_date': '2024-04-15', 'tags': 'main, airtime, utility, utility service', 'title': 'By Airtime'},
            {'name': 'auth0:register', 'publication_name': 'SoftConnect | Sign Up', 'publication_date': '2024-04-15', 'tags': 'authentication, registration, sign up, create account', 'title': 'Sign Up'},
            {'name': 'main:homepage', 'publication_name': 'Soft Connect AI', 'publication_date': '2024-04-15', 'tags': 'Home,homepage, index, website', 'title': 'Homepage'},
            {'name': 'main:about', 'publication_name': 'About | Soft Connect', 'publication_date': '2024-05-04', 'tags': 'About Soft Connect', 'title': 'About Us'},
            {'name': 'vision:index', 'publication_name': 'Explore computer vision', 'publication_date': '2024-05-24', 'tags': 'Image | Compueter Vision', 'title': 'Image | Visoion'}


        ]

    def location(self, item):
        # Reverse the URL based on the URL name
        return reverse(item['name'])

    #def lastmod(self, item):
        # Optional: You can implement lastmod method to return the last modification time for each item
        # Example: return some_last_modification_time

    #def changefreq(self, item):
        # Optional: You can implement changefreq method to return the change frequency for each item
        # Example: return 'daily'

    #def priority(self, item):
        # Optional: You can implement priority method to return the priority for each item
        # Example: return 1.0

