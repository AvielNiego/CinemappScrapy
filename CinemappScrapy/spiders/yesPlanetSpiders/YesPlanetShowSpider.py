from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider
from CinemappScrapy.spiders.yesPlanetSpiders.cookie_value import cookie


class YesPlanetTheaterSpider(ShowsSpider):
    name = "YesPlanet_Shows_Spider"

    def get_host(self):
        return "http://www.yesplanet.co.il"

    def get_shows_and_theater_data_url(self):
        return "http://cinemappebapp-env.us-west-2.elasticbeanstalk.com/yesplanet/presentations"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse,
                          cookies=cookie)
        return [request]
