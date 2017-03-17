# coding=utf-8
import json
import time

import scrapy
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.http import Response

from CinemappScrapy.items import MovieItem


class MovieSpider(scrapy.Spider):
    name = 'CinemaCity_Movies_Spider'

    CINEMA_CITY_MOBILE_HOST = "http://m.cinema-city.co.il"
    MOVIES_URL = CINEMA_CITY_MOBILE_HOST + "/refreshParam"
    MOVIE_DESCRIPTION_URL = "http://www.cinema-city.co.il/featureInfo"
    CINEMA_CITY_POSTER_URL = "http://ccil-media.internet-bee.com/Feats/med/"

    CAT_HORROR = u"אימה"
    CAT_ACTION = u"מתח/פעולה"
    CAT_DRAMA = u"דרמה/איכות"
    CAT_COMEDY = u"קומדיה/רומנטית"
    CAT_CHILDREN = u"ילדים"
    CAT_DISPLAYS = u"ארועים/מופעים"
    CAT_MOVIES = u"סרטים"
    IGNORED_CATEGORIES_LIST = [CAT_DISPLAYS, CAT_MOVIES, ""]

    def __init__(self, *a, **kw):
        super(MovieSpider, self).__init__(*a, **kw)
        self._categories = []

    def start_requests(self):
        request = FormRequest(self.MOVIES_URL,
                              formdata={"refreshFlg": "1", "timeStamp": str((int(round(time.time() * 1000))))},
                              callback=self.parse)
        return [request]

    def parse(self, response):
        """
        :type response: Response
        """
        response_dict = json.loads(response.body)
        self._categories = response_dict["cats"]
        movies_data = self.get_relevant_movies(response_dict["schedFeat"])
        for movie_data in movies_data:
            yield self.get_parse_movie_request(movie_data)

    def get_relevant_movies(self, movies):
        return [movie for movie in movies if self.has_relevant_categories(movie["ex"])]

    def has_relevant_categories(self, movie_id):
        movie_categories = set(self.get_categories(movie_id))
        return len(movie_categories.intersection(self.IGNORED_CATEGORIES_LIST)) == 0

    def get_parse_movie_request(self, movie_data):
        movie = MovieItem(movie_id=movie_data["ex"],
                          title=self.clean_movie_name(movie_data["n"]),
                          year=movie_data["y_ds"],
                          genre=self.get_categories(movie_data["ex"]),
                          poster_url=self.CINEMA_CITY_POSTER_URL + movie_data["fn"],
                          age_limit=movie_data["rn"],
                          length=movie_data["len"])
        return Request(self.MOVIE_DESCRIPTION_URL + "?featureCode=" + str(movie_data["ex"]),
                       callback=self.parse_movie, meta={"movie": movie}, dont_filter=True)

    def clean_movie_name(self, movie_name):
        """
        :type movie_name: str
        """
        for sub in [u"אנגלית", u"אנגלי", u"מדובב"]:
            if sub in movie_name:
                movie_name = movie_name.replace(sub, "")
        return movie_name.strip()

    def get_categories(self, movie_id):
        return [cat["n"] for cat in self._categories if self._is_movie_in_category(movie_id, cat)]

    def _is_movie_in_category(self, movie_id, category):
        movies_in_cat = category["FC"]
        return movie_id in movies_in_cat and category["n"] != u"סרטים"

    def parse_movie(self, response):
        """
        :type response: Response
        """
        movie = response.meta["movie"]
        movie["eng_title"] = self.get_eng_title(response)
        movie["summary"] = self.get_summary(response)
        movie["trailer"] = self.get_trailer(response)
        # yield self._imdb_request.get_request(movie)
        yield movie

    def get_summary(self, response):
        """
        :type response: Response
        """
        return " ".join(response.xpath("//div[@class='feature_synopsis']//*/text()").extract()).strip()

    def get_trailer(self, response):
        """
        :type response: Response
        """
        trailer_links = response.css('a[class*=featureTrailerLinkVisible]::attr(href)').extract()
        if len(trailer_links) > 0:
            return self.extract_youtube_link_from_text(trailer_links)
        return ""

    def extract_youtube_link_from_text(self, trailer_links):
        return trailer_links[0].split("'")[1] if "javascript" in trailer_links[0] else trailer_links[0]

    def get_eng_title(self, response):
        """
            :type response: Response
        """
        return " ".join(response.css(".popup_feature_adname::text").extract()).strip()
