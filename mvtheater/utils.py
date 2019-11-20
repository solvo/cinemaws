import requests
import random
# http://www.omdbapi.com/?apikey=bc53c055&s=Hulk&type=movie&r=json&page=1
from django.utils import timezone

from mvtheater.models import Movies, Matinees, Cinemas
from mvtheater.serializers import Movies_serializer, Matinees_serializer, Custom_Matinees_serializer

api_key = 'bc53c055&s'
url = f'http://www.omdbapi.com/?apikey={api_key}'
page = 1
search_title = ["Batman","Joker","Spider-Man","Superman","Deadpool","Fast","Train","Star"]

def save_movies_into_db(movies):
    movies_names = []
    for movie in movies:
        data = {'name': movie['Title'], 'imdbid': movie['imdbID'], 'release_date': movie['Year']}
        movie_serializer = Movies_serializer(data=data,context={'request':None})
        if movie_serializer.is_valid():
            movie_serializer.save()
            movies_names.append(movie_serializer.data.get('name'))

    return Movies.objects.filter(name__in = movies_names)

def get_movies_from_api(page=1):
    r = requests.get(f'{url}&s={search_title[random.randrange(len(search_title)-1)]}&'
                     f'type=movie&r=json&page={page}')
    search_results = r.json()
    movies = search_results['Search']
    if Movies.objects.filter(name=movies[0]['Title']).exists():
        return get_movies_from_api(page=page+1)
    movies_queryset = save_movies_into_db(movies)

    return movies_queryset

def get_movie_details_from_api(movieID):
    r = requests.get(f'{url}&i={movieID}&r=json')
    movie_details = r.json()
    return movie_details

def check_for_matinees(date):
    matinees = Matinees.objects.filter(data_time__date = date.date())
    if matinees.count() != 0: #there matinees on specified date
        return matinees
    else: # there isnt matinees on specified date, then create new matinees
        return create_matinee(schedule=date,movies=get_movies_from_api())

def create_matinee_on_schedule(schedule = timezone.now().replace(hour=12,minute=30,second=00),matinee_quantity = 3,*args,**kwargs):
    cinema = kwargs.get('cinema')
    movie = kwargs.get('movie')
    for lp in range(matinee_quantity):
        matinee = Custom_Matinees_serializer(
            data={'cinema': cinema.pk, 'movie': movie.pk, 'data_time': schedule, 'cost': 2500})
        if matinee.is_valid(raise_exception=True):
            matinee.save()
            schedule = schedule + timezone.timedelta(hours=2)

def create_matinee(schedule = None,movies=None):
    cinemas = Cinemas.objects.all()

    movies_list = list(movies)
    if cinemas and movies_list[:cinemas.count()]:
        for cinema in cinemas:
            if schedule:
                create_matinee_on_schedule(schedule=schedule,cinema=cinema,movie=movies_list.pop())
            else:
                create_matinee_on_schedule(cinema=cinema,movie=movies_list.pop())

        return Matinees.objects.filter(data_time__date=schedule.date())