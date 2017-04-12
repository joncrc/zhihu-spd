# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    locations = scrapy.Field()
    employments = scrapy.Field()
    gender = scrapy.Field()
    educations = scrapy.Field()
    business = scrapy.Field()
    description = scrapy.Field()
    voteup_count = scrapy.Field()
    thanked_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_count = scrapy.Field()
    answer_count = scrapy.Field()
    articles_count = scrapy.Field()
    favorited_count = scrapy.Field()

    url_token = scrapy.Field()
    name = scrapy.Field()
    user_type = scrapy.Field()
    headline = scrapy.Field()
    avatar_url = scrapy.Field()
