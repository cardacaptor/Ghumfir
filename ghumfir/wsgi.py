"""
WSGI config for ghumfir project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from recommendation.content_based import ContentBasedRecommendation
from scraper.scraper import Scraper
from seeder.generate_from_csv import GenerateFromCSV
from seeder.random_data_feed import RandomDataFeed

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghumfir.settings')

application = get_wsgi_application()

ContentBasedRecommendation() 
# Scraper(RandomDataFeed()).generateOrLoad()
Scraper(GenerateFromCSV()).generateOrLoad()
