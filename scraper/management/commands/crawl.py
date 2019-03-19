from django.core.management.base import BaseCommand
from ...tasks import start_crawl


class Command(BaseCommand):
    help = 'Run TweetSpider crawler process by celery task'

    def handle(self, *args, **options):
        start_crawl.apply()
        print('Done')
