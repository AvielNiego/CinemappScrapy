from scrapy import Request

from CinemappScrapy.spiders.globalSpiders.TheaterSpider import TheaterSpider


class RavHenTheaterSpider(TheaterSpider):
    def get_logo_url(self):
        return "http://ticketnet.co.il/imgs/GIF/Affiliates/Rav-Hen.co.il.gif"

    name = "RavHen_Theater_Spider"

    def get_host(self):
        return "http://www.rav-hen.co.il/"

    def start_requests(self):
        request = Request(self.get_shows_and_theater_data_url(), callback=self.parse)
        return [request]
