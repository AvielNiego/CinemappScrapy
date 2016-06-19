from CinemappScrapy.spiders.globalSpiders.TheaterSpider import TheaterSpider


class CinemaCityTheaterSpider(TheaterSpider):
    name = "CinemaCity_Theater_Spider"

    def get_host(self):
        return "http://cinema-city.co.il"
