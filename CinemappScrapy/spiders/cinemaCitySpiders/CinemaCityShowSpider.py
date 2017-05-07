import requests

from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider


class CinemaCityShowSpider(ShowsSpider):
    name = "CinemaCity_Shows_Spider"
    MOVIE_MAPPING = None

    def get_host(self):
        return "http://91.202.171.158:5000"

