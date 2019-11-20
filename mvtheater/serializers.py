from django.contrib.auth.models import User
from rest_framework import serializers

from mvtheater.models import Clients, Movies, Cinemas, Matinees, Tickets

class User_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'date_joined',
        )

class Clients_serializer(serializers.HyperlinkedModelSerializer):
    user = User_serializer(read_only=True)
    class Meta:
        model = Clients
        fields = ('id',
                  'url',
                  'born_date',
                  'user',)

class Cinemas_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cinemas
        fields = ('id',
                  'url',
                  'name',
                  'seating_capacity',)

class Matinees_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Matinees
        fields = ('id',
                  'url',
                  'cinema',
                  'movie',
                  'data_time',
                  'cost',)

class Tickets_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tickets
        fields = ('id',
                  'url',
                  'matinee',
                  'client',
                  'qrcode',
                  'state',)


class Custom_Matinees_serializer(serializers.ModelSerializer):
    class Meta:
        model = Matinees
        fields = (
                  'cinema',
                  'movie',
                  'data_time',
                  'cost',)


class Movies_serializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='movdet',
            lookup_field='pk'
        )

    class Meta:
        model = Movies
        fields = ('url',
                  'name',
                  'imdbid',
                  'release_date',)

    def create(self, validated_data):
        movie = Movies(
                    name=validated_data['name'],
                    imdbid=validated_data['imdbid'],
                    release_date = validated_data['release_date']
                    )
        movie.save()
        return movie