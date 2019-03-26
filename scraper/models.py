from django.db import models
from nltk.stem.snowball import RussianStemmer, EnglishStemmer
from ukr_stemmer import UkrainianStemmer
from config import constants


class TimeStamped(models.Model):
    """ An abstract base class model that provides self updating """

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TWAccount(models.Model):
    """ Twitter account model """

    name = models.CharField(max_length=constants.account_name_max_length, unique=True)
    objects = models.Manager()

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.name


class Keyword(models.Model):
    """ Search word model """

    keyword = models.CharField(max_length=constants.tweet_keyword_max_length, unique=True)
    language = models.CharField(max_length=2,
                                choices=(('ru', 'Russian'), ('uk', 'Ukrainian'), ('en', 'English'), ('no', 'Not stem')))
    objects = models.Manager()

    class Meta:
        db_table = 'keywords'

    def __str__(self):
        return self.keyword

    def stem_keyword(self):
        """ Stem keyword by Porter or Snowball stemmers """

        if self.language == 'uk':
            self.keyword = UkrainianStemmer(self.keyword).stem_word()
            return

        elif self.language == 'ru':
            stemmer = RussianStemmer()

        elif self.language == 'en':
            stemmer = EnglishStemmer()

        else:
            return

        self.keyword = stemmer.stem(self.keyword)

    def save(self, *args, **kwargs):
        self.keyword = self.keyword.lower()
        self.stem_keyword()
        return super().save(*args, **kwargs)


class Tweet(TimeStamped):
    """ Twitter message model """

    text = models.TextField(unique=True)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    account = models.ForeignKey(TWAccount, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = 'tweets'

    def __str__(self):
        if len(self.text) <= constants.tweet_preview_length:
            return '{0}: {1}'.format(self.account, self.text)

        return '{0}: {1}...'.format(self.account, self.text[:constants.tweet_preview_length])
