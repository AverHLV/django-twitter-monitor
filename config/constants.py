from unipath import Path

base_dir = Path(__file__).ancestor(2)
secret_filename = base_dir.child('config').child('secret.json')

# scraper
account_name_max_length = 50
tweet_preview_length = 40
tweet_keyword_max_length = 30
tweet_min_length = 15

spider_settings = {
    'ROBOTSTXT_OBEY': True,
    'LOG_FILE': 'spider.log',
    'ITEM_PIPELINES': {'scraper.pipelines.ScraperPipeline': 300}
}
