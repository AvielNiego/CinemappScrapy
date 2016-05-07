from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider


class CinemaCityShowSpider(ShowsSpider):
    name = "cc_s"

    def get_host(self):
        return "http://cinema-city.co.il"
