# Django Twitter monitor
Django + Scrapy project for monitoring tweets from specified Twitter accounts for specific keywords.

## Apps
* scraper: main app, implements necessary models and Scrapy spider.

## Tasks
Backend tasks powered by celery and django-celery-beat scheduler.

## Usage
Spider can be executed from celery-beat as periodic task or manually by command:
```
python manage.py crawl
```