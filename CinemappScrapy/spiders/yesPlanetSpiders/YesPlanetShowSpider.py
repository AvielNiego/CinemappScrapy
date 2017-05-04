from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider


class YesPlanetTheaterSpider(ShowsSpider):
    name = "YesPlanet_Shows_Spider"

    def get_host(self):
        return "http://35.185.234.255:5000"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]
