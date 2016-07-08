# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class MovieItem(scrapy.Item):
    eng_title = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(output_processor=TakeFirst())
    genre = scrapy.Field(output_processor=TakeFirst())
    poster_url = scrapy.Field(output_processor=TakeFirst())
    age_limit = scrapy.Field(output_processor=TakeFirst())
    length = scrapy.Field(output_processor=TakeFirst())
    summary = scrapy.Field(output_processor=TakeFirst())
    trailer = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    movie_id = scrapy.Field(output_processor=TakeFirst())
    imdb_rating = scrapy.Field(output_processor=TakeFirst())


class TheaterItem(scrapy.Item):
    location = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    theater_id = scrapy.Field(output_processor=TakeFirst())
    logo_url = scrapy.Field(output_processor=TakeFirst())


class ShowItem(scrapy.Item):
    pc = scrapy.Field(output_processor=TakeFirst())
    venue_type = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    theater_id = scrapy.Field(output_processor=TakeFirst())
    movie_id = scrapy.Field(output_processor=TakeFirst())
