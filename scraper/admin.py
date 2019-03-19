from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from config import constants
from .models import TWAccount, Keyword, Tweet


@admin.register(TWAccount)
class TWAccountAdmin(admin.ModelAdmin):
    ordering = 'name',
    search_fields = 'name',


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    ordering = 'keyword',
    search_fields = 'keyword',


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    ordering = '-created',
    readonly_fields = 'created',
    list_filter = 'created',
    search_fields = 'text',

    def get_search_results(self, request, queryset, search_term):
        """ Custom tweet search """

        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if len(search_term) <= constants.account_name_max_length:
            # search by Twitter account name

            try:
                account = TWAccount.objects.get(name=search_term)

            except ObjectDoesNotExist:
                return queryset, use_distinct

            queryset |= Tweet.objects.filter(account=account)

        elif len(search_term) <= constants.tweet_keyword_max_length:
            # search by keyword

            queryset |= Tweet.objects.filter(keyword=search_term)

        return queryset, use_distinct
