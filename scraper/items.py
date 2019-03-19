from scrapy_djangoitem import DjangoItem
from .models import Tweet


class TweetItem(DjangoItem):
    django_model = Tweet
