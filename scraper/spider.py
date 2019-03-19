# coding: utf8
from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.crawler import CrawlerProcess
from re import sub, search
from config import constants
from utils import secret_dict
from .items import TweetItem


def run_spider(accounts, keywords=constants.keywords):
    """
    Run TweetSpider as new process

    :param accounts: TWAccount model objects
    :param keywords: tuple of strings for searching in tweets
    """

    process = CrawlerProcess(constants.spider_settings)
    process.crawl(TweetSpider, accounts=accounts, keywords=keywords)
    process.start()


class TweetSpider(Spider):
    """ Twitter.com spider for scraping tweets from specified accounts """

    name = 'tweets'
    allowed_domains = 'twitter.com',
    start_urls = 'https://mobile.twitter.com/login',
    lf_message = 'The username and password you entered did not match our records. Please double-check and try again.'

    def __init__(self, accounts, keywords, tweet_min_length=constants.tweet_min_length, *args, **kwargs):
        """
        TweetSpider initialization

        :param accounts: TWAccount model queryset
        :param keywords: tuple of strings for searching in tweets
        :param tweet_min_length: minimum possible tweet length
        """

        super().__init__(*args, **kwargs)
        self.accounts = accounts
        self.keywords = keywords
        self.tweet_min_length = tweet_min_length
        self.credentials = {'email': secret_dict['tw_email'], 'password': secret_dict['tw_password']}

    def parse(self, response):
        """ Log in Twitter account by specified credentials """

        return FormRequest.from_response(
            response,
            callback=self.after_login,
            formdata={
                'session[username_or_email]': self.credentials['email'],
                'session[password]': self.credentials['password']
            }
        )

    def after_login(self, response):
        """ Check authentication result and start scraping """

        if response.xpath('//div[contains(text(), "{0}")]'.format(self.lf_message)).get() is not None:
            self.logger.critical('Login failed')
            return

        self.logger.info('Logged in successfully')

        for account in self.accounts:
            yield Request('https://mobile.twitter.com/{0}'.format(account.name), callback=self.parse_tweets)

    def parse_tweets(self, response):
        current_account = self.accounts.get(name=response.url[response.url.rfind('/') + 1:])

        for tweet_div in response.xpath('//div[@class="dir-ltr"]'):
            tweet_text = self.clear_text(''.join(tweet_div.xpath('text()').getall()))

            if tweet_text is None:
                continue

            keyword = self.search_for_keywords(tweet_text)

            if keyword is None:
                continue

            tweet = TweetItem()
            tweet['text'] = tweet_text
            tweet['keyword'] = keyword
            tweet['account'] = current_account
            yield tweet

    def clear_text(self, text):
        """ Clear text form non-cyrillic, non-latin and non-digit symbols except spaces """

        text = sub(r'[^a-zа-я0-9 ]', '', text.lower())
        text = sub(r' {2,}', ' ', text)

        if len(text) < self.tweet_min_length:
            return

        if text[0] == ' ':
            text = text[1:]

        if text[-1] == ' ':
            text = text[:-1]

        if len(text) < self.tweet_min_length:
            return

        return text

    def search_for_keywords(self, text):
        for keyword in self.keywords:
            if search(keyword, text) is not None:
                return keyword
