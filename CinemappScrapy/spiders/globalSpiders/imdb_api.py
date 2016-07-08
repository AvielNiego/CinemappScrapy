# coding=utf-8
import json
import urllib

import requests
from scrapy import Request

from CinemappScrapy.items import MovieItem

MOVIE_MAPPING_URL = "http://django-env.wpcqmjpmpv.us-west-2.elasticbeanstalk.com/movies/"

GENRE_TRANSLATE = {
    "Action": u"אקשן",
    "Animation": u"מצוייר",
    "Comedy": u"קומדיה",
    "Documentary": u"דוקומנטרי",
    "Family": u"משפחה",
    "Film-Noir": u"אפל",
    "Horror": u"אימה",
    "Romance": u"רומנטי",
    "Sport": u"ספורט",
    "War": u"מלחמה",
    "Adventure": u"הרפתקאות",
    "Biography": u"ביוגרפי",
    "Crime": u"פשע",
    "Drama": u"דרמה",
    "Fantasy": u"פנטזיה",
    "History": u"היסטורי",
    "Music": u"מוזיקה",
    "Musical": u"מוזיקלי",
    "Mystery": u"תעלומה",
    "Sci-Fi": u"מדע בדיוני",
    "Thriller": u"מתח",
    "Western": u"מערבון",
    "Short": u"קצר"}

IMDB_API_URL = "http://www.omdbapi.com/"


class ImdbRequest:
    def __init__(self):
        self._movie_mapping = None

    def get_request(self, movie):
        """
        :type movie: MovieItem
        """
        mapped_movie = self._get_movie_from_mapping(movie)
        if mapped_movie and mapped_movie['imdb_id']:
            return Request(self._get_imdb_api_url_for_id(mapped_movie['imdb_id']), callback=self._imdb_api_parser,
                           meta={"movie": movie},
                           dont_filter=True)
        else:
            self._add_to_movie_mapping(movie)
            return movie

    def _add_to_movie_mapping(self, movie):
        imdb_data = requests.get(self._get_imdb_api_url_for_name(movie["eng_title"])).json()
        if imdb_data["Response"] == "True":
            requests.get(MOVIE_MAPPING_URL + "add/cinema?" + urllib.urlencode({'movie_id': movie["movie_id"],
                                                                               'movie_title': movie["eng_title"].encode(
                                                                                   'utf-8'),
                                                                               'imdb_id': imdb_data["imdbID"],
                                                                               'imdb_title': imdb_data["Title"].encode(
                                                                                   'utf-8')}))
        else:
            requests.get(MOVIE_MAPPING_URL + "add/cinema?" + urllib.urlencode({'movie_id': movie["movie_id"],
                                                                               'movie_title': movie["eng_title"].encode(
                                                                                   'utf-8')}))

    def _get_movie_from_mapping(self, movie):
        """
        :rtype: dict
        """
        filtered_mapping = filter(lambda m: m["cinema_city_id"] == str(movie["movie_id"]), self._get_movie_mapping())
        return filtered_mapping[0] if len(filtered_mapping) > 0 else None

    def _get_movie_mapping(self):
        if not self._movie_mapping:
            self._load_movie_mapping()
        return self._movie_mapping

    def _load_movie_mapping(self):
        self._movie_mapping = requests.get(MOVIE_MAPPING_URL).json()

    def _attach_with_imdb_id(self, movie, imdb_id):
        pass

    def _get_imdb_api_url_for_id(self, imdb_id):
        return IMDB_API_URL + "?i=" + imdb_id + "&plot=short"

    def _imdb_api_parser(self, response):
        """
        :type response: Response
        """
        imdb_data = json.loads(response.body)
        movie = response.meta["movie"]
        self._add_imdb_data_to_movie(imdb_data, movie)
        yield movie

    def _add_imdb_data_to_movie(self, imdb_data, movie):
        if imdb_data["Response"] == "True":
            movie["poster_url"] = imdb_data["Poster"] if "Poster" in imdb_data.keys() and imdb_data["Poster"] != "N/A" else movie["poster_url"]
            movie["imdb_rating"] = imdb_data["imdbRating"] if "imdbRating" in imdb_data.keys() else movie["imdb_rating"]
            movie["imdb_rating"] = "" if imdb_data["imdbRating"] == "N/A" else movie["imdb_rating"]
            movie["genre"] = self._translate_genres(imdb_data["Genre"].split(",")) if "Genre" in imdb_data.keys() else \
                movie["genre"]

    def _translate_genres(self, english_genres):
        """
        :type english_genres: list
        """
        english_genres = map(lambda genre: genre.strip(), english_genres)
        translated_genres = map(lambda genre: GENRE_TRANSLATE[genre] if genre in GENRE_TRANSLATE.keys() else genre,
                                english_genres)
        return translated_genres

    def _get_imdb_api_url_for_name(self, movie_name):
        return IMDB_API_URL + "?plot=short&t=" + movie_name
