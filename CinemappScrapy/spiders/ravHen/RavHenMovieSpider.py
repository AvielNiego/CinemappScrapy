# coding=utf-8
import json
import urllib

import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from CinemappScrapy.items import MovieItem
from CinemappScrapy.spiders.ravHen.rav_hen_movie_parser import RavHenMovieParser

MOVIE_DESCRIPTION_URL = "http://rav-hen.co.il"


class RavHenMovieSpider(scrapy.Spider):
    name = "RavHen_Movies_Spider"

    HOST = "http://www.rav-hen.co.il/"

    def start_requests(self):
        request = Request(self.HOST, callback=self.parse)
        return [request]

    def parse(self, response):
        """
        :type response: Response
        """
        for movie_div_info in response.xpath('//div[@class="featureDiv"]'):
            data_info = json.loads(movie_div_info.xpath("@data-info").extract_first(default='{"distribcode": "1"}'))
            movie_id = data_info["distribcode"]
            heb_name = urllib.unquote(data_info["urln"])
            movie_data_url = movie_div_info.xpath("@data-feature_url").extract_first()
            yield self.parse_movie(movie_id, movie_data_url, heb_name)

    def parse_movie(self, movie_id, movie_data_url, heb_name):
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
        l.add_value("title", heb_name)
        l.add_value("imdb_rating", "")
        l.add_value("imdb_rating", "")
        return Request(MOVIE_DESCRIPTION_URL + movie_data_url, callback=RavHenMovieParser().parse_movie_details,
                       meta={"movie": l.load_item()}, dont_filter=True)

    def get_end_title(self, url):
        return urllib.unquote(url.split('/')[-1])
