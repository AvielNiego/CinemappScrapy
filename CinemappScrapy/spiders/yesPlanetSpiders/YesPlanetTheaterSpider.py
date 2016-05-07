from CinemappScrapy.spiders.globalSpiders.TheaterSpiser import TheaterSpider
from CinemappScrapy.spiders.yesPlanetSpiders.cookie_value import cookie


class YesPlanetTheaterSpider(TheaterSpider):
    name = "YesPlanet Theater Spider"

    def get_host(self):
        return "http://www.yesplanet.co.il"

    def start_requests(self):
        from scrapy import Request
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse,
                          cookies=cookie)
        return [request]
