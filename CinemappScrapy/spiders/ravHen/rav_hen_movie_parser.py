
class RavHenMovieParser:
    def __init__(self):
        pass

    def parse_movie_details(self, response):
        movie = response.meta["movie"]
        if response.status == 404:
            return movie
        movie["year"] = self._get_year(response)
        movie["genre"] = self._get_genre(response)
        movie["poster_url"] = self._get_poster(response)
        movie["age_limit"] = self._get_age_limit(response)
        movie["length"] = self._get_length(response)
        movie["summary"] = self._get_summary(response)
        movie["trailer"] = self._get_trailer(response)
        return movie

    def _get_year(self, response):
        try:
            features = self._get_features(response)
            return int(features[6][1].split()[1])
        except:
            return 0

    def _get_features(self, response):
        try:
            return [x.xpath('div/text()').extract() for x in response.xpath("//div[@class='feature_info']/div")]
        except:
            return ''

    def _get_genre(self, response):
        try:
            features = self._get_features(response)
            return [x.strip() for x in features[0][1].split(',')]
        except:
            return []

    def _get_poster(self, response):
        try:
            return response.xpath("//div[@class='poster_holder']/img/@src").extract()[0]
        except:
            return ''

    def _get_age_limit(self, response):
        try:
            features = self._get_features(response)
            return features[3][1]
        except:
            return ''

    def _get_length(self, response):
        try:
            features = self._get_features(response)
            return int(features[1][1])
        except:
            return 0

    def _get_summary(self, response):
        try:
            return response.xpath("//div[@class='feature_info_synopsis ScrollPane']/p/text()").extract()[0]
        except:
            return ''

    def _get_trailer(self, response):
        try:
            full_url = response.xpath("//iframe[@class='youtube-player']/@src").extract()[0]
            return "http://youtube.com/" + full_url[:full_url.index('?')].split('/')[-1]
        except:
            return ''
