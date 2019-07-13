# Django Twitter monitor
Django + Scrapy project for monitoring tweets from specified Twitter accounts for specific keywords.
The developed monitoring system searches the keywords in the tweets of the specified Twitter accounts with a certain
periodicity, for example, 60 minutes.

Accounts, keywords and tweets are Django models. Interaction with them occurs through the admin panel of Django.

Before adding a keyword, you can perform stemming (highlighting the stem of the word),
Ukrainian, Russian and English are supported. Stemming can be omitted if the word is an abbreviation or proper name.

Implemented login to the given Twitter account and further search in the texts of the latest tweets added
to the accounts with the help of the so-called "spider" (scrapy.Spider).

## Apps
* scraper: main app, implements necessary models and Scrapy spider.

## Tasks
Backend tasks powered by celery and django-celery-beat scheduler.

## Usage
Spider can be executed from celery-beat as periodic task or manually by command:
```
python manage.py crawl
```
