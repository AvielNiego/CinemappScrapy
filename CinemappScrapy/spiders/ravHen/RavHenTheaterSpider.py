from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.TheaterSpider import TheaterSpider


class RavHenTheaterSpider(TheaterSpider):
    def get_logo_url(self):
        return "http://cinemappebapp-env.us-west-2.elasticbeanstalk.com/static/theaters_logo/yes_planet_logo.jpg"

    name = "RavHen_Theater_Spider"

    def get_host(self):
        return "http://www.rav-hen.co.il/"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]
