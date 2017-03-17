import requests

from CinemappScrapy.spiders.globalSpiders.ShowsSpider import ShowsSpider


class CinemaCityShowSpider(ShowsSpider):
    name = "CinemaCity_Shows_Spider"
    MOVIE_MAPPING = None

    def get_host(self):
        return "http://cinema-city.co.il"

    def get_shows_map(self):
        if not CinemaCityShowSpider.MOVIE_MAPPING:
            CinemaCityShowSpider.MOVIE_MAPPING = requests.get(
                "http://cinemappebapp-env.us-west-2.elasticbeanstalk.com/movies").json()
        return CinemaCityShowSpider.MOVIE_MAPPING
