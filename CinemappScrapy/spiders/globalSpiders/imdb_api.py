# coding=utf-8
GENRE_TRANSLATE = {
    "Action": u"אקשן",
    "Animation": u"מצוייר",
    "Comedy": u"קומדיה",
    "Documentary": u"דוקומנטרי",
    "Family": u"משפחה",
    "Film-Noir": u"אפל",
    "Horror": u"אימה",
    "Romance": u"רומנטי",
    "Sport": u"ספורט",
    "War": u"מלחמה",
    "Adventure": u"הרפתקאות",
    "Biography": u"ביוגרפי",
    "Crime": u"פשע",
    "Drama": u"דרמה",
    "Fantasy": u"פנטזיה",
    "History": u"היסטורי",
    "Music": u"מוזיקה",
    "Musical": u"מוזיקלי",
    "Mystery": u"תעלומה",
    "Sci-Fi": u"מדע בדיוני",
    "Thriller": u"מתח",
    "Western": u"מערבון"}

IMDB_API_URL = "http://www.omdbapi.com/"


def get_imdb_api_query(movie_name):
    return IMDB_API_URL + "?plot=short&t=" + movie_name


def translate_genres(english_genres):
    """
    :type english_genres: list
    """
    english_genres = map(lambda genre: genre.strip(), english_genres)
    translated_genres = map(lambda genre: GENRE_TRANSLATE[genre] if genre in GENRE_TRANSLATE.keys() else genre, english_genres)
    return translated_genres


def add_imdb_data_to_movie(imdb_data, movie):
    if imdb_data["Response"] == "True":
        movie["poster_url"] = imdb_data["Poster"] if "Poster" in imdb_data.keys() else movie["poster_url"]
        movie["imdb_rating"] = imdb_data["imdbRating"] if "imdbRating" in imdb_data.keys() else movie["imdb_rating"]
        movie["imdb_rating"] = "" if imdb_data["imdbRating"] == "N/A" else movie["imdb_rating"]
        movie["genre"] = translate_genres(imdb_data["Genre"].split(",")) if "Genre" in imdb_data.keys() else movie["genre"]