from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider


class RavHenTheaterSpider(ShowsSpider):
    name = "RavHen_Shows_Spider"

    def get_host(self):
        return "http://www.rav-hen.co.il/"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]
