import json
import urllib

import scrapy

from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from CinemappScrapy.items import MovieItem


class YesPlanetMovieSpider(scrapy.Spider):
    name = "YesPlanet_Movies_Spider"

    HOST = "http://104.199.113.249:5000"

    def start_requests(self):
        request = Request(self.HOST, callback=self.parse)
        return [request]

    def parse(self, response):
        """
        :type response: Response
        """
        for movie_div_info in response.xpath('//*[@class="featuresCarouselExtended"]/div[2]/div/div[1]/ul/li/div'):
            movie_id = json.loads(movie_div_info.xpath("@data-info").extract_first(default='{"distribcode": "1"}'))[
                "distribcode"]
            movie_data_url = movie_div_info.xpath("@data-feature_url").extract_first()
            yield self.parse_movie(movie_id, movie_data_url)

    def parse_movie(self, movie_id, movie_data_url):
        l = ItemLoader(item=MovieItem())
        l.add_value("movie_id", movie_id)
        l.add_value("year", "")
        l.add_value("eng_title", self.get_end_title(movie_data_url))
        l.add_value("genre", "")
        l.add_value("poster_url", "")
        l.add_value("age_limit", "")
        l.add_value("length", "")
        l.add_value("summary", "")
        l.add_value("trailer", "")
        l.add_value("title", "")
        l.add_value("poster_url", "")
        l.add_value("imdb_rating", "")
        l.add_value("imdb_rating", "")
        l.add_value("genre", "")
        return l.load_item()

    def get_end_title(self, url):
        return urllib.unquote(url.split('/')[-1])
