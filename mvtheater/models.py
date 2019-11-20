from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
from stripeapp.models import Transaction



class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name=_("User"))
    born_date = models.DateField(verbose_name=_("Born Date"))

    def __str__(self):
        name = self.user.get_full_name()
        if not name:
            name = self.user.username
        return name

    class Meta:
        ordering = ["user"]


class Movies(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name=_("Movie name"))
    imdbid = models.CharField(max_length=15,null=True, blank=True,
                                   verbose_name=_("movie id"))
    release_date = models.CharField(max_length=4,verbose_name=_("Release date"))

    def __str__(self):
        return f'{self.name} - {self.release_date}'

    class Meta:
        ordering = ["release_date"]


class Cinemas(models.Model):
    #movie = models.ManyToManyField(Movies)
    name = models.CharField(max_length=200,
                            verbose_name=_("Cinema name"))
    seating_capacity = models.CharField(max_length=200,
                                        verbose_name=_("Seating capacity"))

    def __str__(self):
        return self.name

class Matinees(models.Model):
    cinema = models.ForeignKey(Cinemas, on_delete=models.CASCADE,
                               verbose_name=_("Cinema"))
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE,
                              verbose_name=_("Movie name"))
    data_time = models.DateTimeField(verbose_name=_("DateTime"))
    cost = models.FloatField(verbose_name=_("Cost"))

    def __str__(self):
        return "Cinema %s at %s" % (self.cinema, self.data_time.strftime("%d/%m/%Y - %H:%M:%S"))

    class Meta:
        ordering = ["data_time"]


class Tickets(models.Model):
    matinee = models.ForeignKey(Matinees, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name=_("Matinee"),related_name='tickets')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE,
                               verbose_name=_("Client"),null=True,blank=True)
    qrcode = models.ImageField(upload_to='qrcode/', null=True, blank=True,
                               verbose_name=_("QR code"))
    transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='transaction')
    state = models.BooleanField(default=False, verbose_name=_("It was used"))

    def __str__(self):
        if self.client:
            return "Client %s ,ticket for %s at %s." % (self.client.user.first_name,self.matinee.movie,self.matinee.cinema)
        return "Ticket for %s at %s, " % (self.matinee.movie,self.matinee.cinema)

    class Meta:
        ordering = ["matinee"]