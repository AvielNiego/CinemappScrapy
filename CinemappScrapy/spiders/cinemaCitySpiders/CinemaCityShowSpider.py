from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider


class CinemaCityShowSpider(ShowsSpider):
    name = "CinemaCity_Shows_Spider"

    def get_host(self):
        return "http://cinema-city.co.il"
