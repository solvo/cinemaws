import requests
from django.core.management.base import BaseCommand
from django.http import response


class Command(BaseCommand):

    def get_token(self):
        data = {
            'username': 'admin',
            'password': 'Password123'
        }
        r = requests.post('http://127.0.0.1:8000/api/token/', data=data)
        return r.json()['access']

    def handle(self, *args, **options):
        headers = {'Authorization': 'Bearer ' + self.get_token(), }
        requests.post('http://127.0.0.1:8000/rest/cinemas/',
                      headers=headers,
                      data={"name": "cinema_8",
                            "seating_capacity": "45"})
