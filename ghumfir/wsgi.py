"""
WSGI config for ghumfir project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from recommendation.content_based import ContentBasedRecommendation
from recommendation.models import Corpus
from scraper.collected import Collected
from scraper.places import PlacesJson

from scraper.scraper import Scraper
from seeder.generate_from_csv import GenerateFromCSV

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ghumfir.settings')

application = get_wsgi_application()

#to load from start
# Scraper(GenerateFromCSV(override = True, delete = True)).generateOrLoad()
# Collected(GenerateFromCSV(override = True, delete = False)).generateOrLoad()
# PlacesJson(GenerateFromCSV(override = True, delete = False)).generateOrLoad()

#by default
Scraper(GenerateFromCSV(override = False, delete = False)).generateOrLoad()
Collected(GenerateFromCSV(override = False, delete = False)).generateOrLoad()
PlacesJson(GenerateFromCSV(override = False, delete = False)).generateOrLoad()

recommendation = ContentBasedRecommendation() 
# Scraper(RandomDataFeed()).generateOrLoad()
# TfidVectorizerService().testVectorizer()
