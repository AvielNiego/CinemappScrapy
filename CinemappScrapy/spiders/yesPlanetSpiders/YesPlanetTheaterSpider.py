from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.TheaterSpider import TheaterSpider
from CinemappScrapy.spiders.yesPlanetSpiders.cookie_value import cookie


class YesPlanetTheaterSpider(TheaterSpider):
    def get_logo_url(self):
        return "http://django-env.wpcqmjpmpv.us-west-2.elasticbeanstalk.com/static/theaters_logo/yes_planet_logo.jpg"

    name = "YesPlanet_Theater_Spider"

    def get_host(self):
        return "http://www.yesplanet.co.il"

    def get_shows_and_theater_data_url(self):
        return "http://django-env.wpcqmjpmpv.us-west-2.elasticbeanstalk.com/yesplanet/presentations"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse,
                          cookies=cookie)
        return [request]
