import json
from abc import abstractmethod

import scrapy

from scrapy.http import Request
from scrapy.http import Response

from CinemappScrapy.items import TheaterItem


class TheaterSpider(scrapy.Spider):
    name = 't'
    GOOGLE_PLACES_API_HOST = 'https://maps.googleapis.com/maps/api'
    GOOGLE_PLACES_API_SEARCH_PATH = GOOGLE_PLACES_API_HOST + '/place/textsearch/json'
    API_KEY = 'AIzaSyAtPWL05cKG0yMQofkxDea3OPMF1Li7JgM'

    HEBREW_LANG_CODE = 'iw'

    @abstractmethod
    def get_host(self):
        pass

    @abstractmethod
    def get_logo_url(self):
        pass

    def get_shows_and_theater_data_url(self):
        return self.get_host() + "/presentationsJSON"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]

    def parse(self, response):
        """
        :type response: Response
        """
        all_movie_data = json.loads(response.body)
        for theater in self.extract_theaters(all_movie_data):
            yield Request(self.generate_places_api_query(theater["name"]), meta={"theater_info": theater}, callback=self.parse_places_api)

    def generate_places_api_query(self, theater_name):
        return self.GOOGLE_PLACES_API_SEARCH_PATH + "?key=" + self.API_KEY + "&query=" + theater_name + "&language=" + self.HEBREW_LANG_CODE

    def extract_theaters(self, all_movie_data):
        theaters = set()
        for theater_data in all_movie_data['sites']:
            theaters.add(TheaterItem(name=theater_data["sn"], theater_id=theater_data["si"],
                                     logo_url=self.get_logo_url()))
        return theaters

    def parse_places_api(self, response):
        """
        :type response: Response
        """
        theater = response.meta["theater_info"]
        self.add_places_api_data(json.loads(response.body), theater)
        yield theater

    def add_places_api_data(self, places_api_data, theater):
        if places_api_data["status"] == "OK":
            api_result = places_api_data['results'][0]
            theater["location"] = self.get_location(api_result)
        else:
            theater["location"] = {'lat': "0", 'lng': "0"}

    def get_location(self, api_result):
        return {'lat': api_result['geometry']['location']['lat'], 'lng': api_result['geometry']['location']['lng']}
