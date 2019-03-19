from django.db import models
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


class Tweet(TimeStamped):
    """ Twitter message model """

    text = models.TextField(unique=True)
    keyword = models.CharField(max_length=constants.tweet_keyword_max_length)
    account = models.ForeignKey(TWAccount, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        db_table = 'tweets'

    def __str__(self):
        if len(self.text) <= constants.tweet_preview_length:
            return '{0}: {1}'.format(self.account, self.text)

        return '{0}: {1}...'.format(self.account, self.text[:constants.tweet_preview_length])
