from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.TheaterSpider import TheaterSpider


class YesPlanetTheaterSpider(TheaterSpider):
    def get_logo_url(self):
        return "http://cinemappebapp-env.us-west-2.elasticbeanstalk.com/static/theaters_logo/yes_planet_logo.jpg"

    name = "YesPlanet_Theater_Spider"

    def get_host(self):
        return "http://35.185.234.255:5000"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]
