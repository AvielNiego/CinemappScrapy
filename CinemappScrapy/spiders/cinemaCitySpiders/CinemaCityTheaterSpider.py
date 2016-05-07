from CinemappScrapy.spiders.globalSpiders.TheaterSpiser import TheaterSpider


class CinemaCityTheaterSpider(TheaterSpider):
    name = "cc_t"

    def get_host(self):
        return "http://cinema-city.co.il"
