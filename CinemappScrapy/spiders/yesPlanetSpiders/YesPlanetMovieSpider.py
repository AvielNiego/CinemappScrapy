import json

import urllib

import scrapy

from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader

from CinemappScrapy.items import MovieItem
from CinemappScrapy.spiders.globalSpiders import imdb_api
from CinemappScrapy.spiders.globalSpiders.imdb_api import add_imdb_data_to_movie
from CinemappScrapy.spiders.yesPlanetSpiders.cookie_value import cookie


class YesPlanetMovieSpider(scrapy.Spider):
    name = "yp_m"

    HOST = "http://www.yesplanet.co.il"

    def start_requests(self):
        request = Request(self.HOST, callback=self.parse, cookies=cookie)
        return [request]

    def parse(self, response):
        """
        :type response: Response
        """
        for movie_div_info in response.xpath("//*[@id='layer_1_0_110']/div[24]/div/ul/*/div"):
            movie_data_url = movie_div_info.xpath("@data-feature_url").extract_first()
            movie_id = json.loads(movie_div_info.xpath("@data-info").extract_first(default='{"distribcode": "1"}'))["distribcode"]
            yield Request(self.HOST + movie_data_url, callback=self.parse_movie, meta={"movie_id": movie_id})

    def parse_movie(self, response):
        """
        :type response: Response
        """
        l = ItemLoader(item=MovieItem(), response=response)
        l.add_value("movie_id", response.meta["movie_id"])
        l.add_value("year", self.get_year(response))
        l.add_value("eng_title", self.get_end_title(response))
        l.add_xpath("genre", "//*[@id='layer_1_0_0']/div[6]/div/div/div[5]/div[1]/div[1]/div[2]/text()")
        l.add_xpath("poster_url", "//*[@id='layer_1_0_0']/div[6]/div/div/div[4]/div/div/img/@src")
        l.add_xpath("age_limit", "//*[@id='layer_1_0_0']/div[6]/div/div/div[5]/div[1]/div[4]/div[2]/text()")
        l.add_xpath("length", "//*[@id='layer_1_0_0']/div[6]/div/div/div[5]/div[1]/div[2]/div[2]/text()")
        l.add_xpath("summary", "//*[@id='layer_1_0_0']/div[6]/div/div/div[5]/div[2]/p[2]/text()")
        l.add_xpath("trailer", "//iframe[@class='youtube-player']/@src")
        l.add_xpath("title", "//*[@id='layer_1_0_0']/div[6]/div/div/div[3]/text()")
        return Request(imdb_api.get_imdb_api_query(self.get_end_title(response)),
                       meta={"movie_item": l.load_item()}, callback=self.imdb_api_parser)

    def get_year(self, response):
        """
        :type response: Response
        """
        year_and_country = response.xpath("//*[@id='layer_1_0_0']/div[6]/div/div/div[5]/div[1]/div[7]/div[2]").extract_first(default="")
        year = int(filter(str.isdigit, str(year_and_country)))
        return year

    def get_end_title(self, response):
        """
        :type response: Response
        """
        # From the url. Decode the movie name
        return urllib.unquote(response.url.rsplit('/', 1)[-1])

    def imdb_api_parser(self, response):
        """
        :type response: Response
        """
        imdb_data = json.loads(response.body)
        movie = response.meta["movie_item"]
        add_imdb_data_to_movie(imdb_data, movie)
        yield movie
