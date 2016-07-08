import json
from abc import abstractmethod

import datetime
import scrapy
import time
from scrapy.http import FormRequest

from CinemappScrapy.items import ShowItem


class ShowsSpider(scrapy.Spider):
    name = 's'

    @abstractmethod
    def get_host(self):
        pass

    def get_shows_and_theater_data_url(self):
        return self.get_host() + "/presentationsJSON"

    def start_requests(self):
        request = FormRequest(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]

    def parse(self, response):
        """
        :type response: Response
        """
        all_shows_data = json.loads(response.body)
        venue_types = all_shows_data["venueTypes"]
        for theater_data in all_shows_data["sites"]:
            for movie_data in theater_data["fe"]:
                for show_data in movie_data["pr"]:
                    yield self.create_show(movie_data, show_data, theater_data, venue_types)

    def create_show(self, movie_data, show_data, theater_data, venue_types):
        return ShowItem(movie_id=movie_data["dc"],
                        theater_id=theater_data["si"],
                        venue_type=self.get_show_type(show_data, venue_types),
                        date=self.get_show_date_millis(show_data),
                        pc=show_data["pc"])

    def get_show_type(self, show_data, venue_types):
        return venue_types[show_data["vt"]] if venue_types and venue_types[show_data['vt']] else "Normal"

    def get_show_date_millis(self, show_data):
        show_time_date = self._get_show_time_date(show_data)
        if show_time_date.hour <= 5:
            show_time_date = self._add_day(show_time_date)
        return self._unix_time_millis(show_time_date)

    def _get_show_time_date(self, show_data):
        date = show_data['dt']
        show_time_string = date.split(" ")[0] + " " + show_data['tm']
        show_time_date = time.strptime(show_time_string, "%d/%m/%Y %H:%M")
        return datetime.datetime.fromtimestamp(time.mktime(show_time_date))

    def _add_day(self, show_time_date):
        timedelta = datetime.timedelta(days=1)
        show_time_date = show_time_date + timedelta
        return show_time_date

    def _unix_time_millis(self, dt):
        epoch = datetime.datetime.utcfromtimestamp(0)
        return (dt - epoch).total_seconds() * 1000.0
