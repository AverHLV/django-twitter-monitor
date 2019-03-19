from celery import shared_task
from .spider import run_spider
from .models import TWAccount, Keyword


@shared_task(name='Scrape tweets')
def start_crawl():
    run_spider(TWAccount.objects.all(), Keyword.objects.all())
