from .models import Tweet


class ScraperPipeline(object):
    @staticmethod
    def process_item(item, _):
        if Tweet.objects.filter(text=item['text']).exists():
            return

        item.save()
        return item
