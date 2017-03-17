from CinemappScrapy.spiders.globalSpiders.TheaterSpider import TheaterSpider


class CinemaCityTheaterSpider(TheaterSpider):
    def get_logo_url(self):
        return "http://cinemappebapp-env.us-west-2.elasticbeanstalk.com/static/theaters_logo/cinema_city_logo.jpg"

    name = "CinemaCity_Theater_Spider"

    def get_host(self):
        return "http://cinema-city.co.il"
