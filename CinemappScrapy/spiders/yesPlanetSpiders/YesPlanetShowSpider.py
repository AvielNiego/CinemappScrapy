from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider
from CinemappScrapy.spiders.yesPlanetSpiders.cookie_value import cookie


class YesPlanetTheaterSpider(ShowsSpider):
    name = "YesPlanet Shows Spider"

    def get_host(self):
        return "http://www.yesplanet.co.il"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse,
                          cookies=cookie)
        return [request]
