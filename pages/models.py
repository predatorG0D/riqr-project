from datetime import datetime
from uuid import uuid4

import qrcode
from PIL import Image
from django.db import models
from django.contrib.postgres.fields import ArrayField


class PagesManager(models.Manager):
    def create_page(self, name, surname, otchestvo, place_of_birth, place_of_death, date_of_birth, date_of_death,
                    nationality, biography, coords, avatar=None, pictures=None, facts=None, videos=None, price=None, private=None):
        page = self.model(name=name, surname=surname, otchestvo=otchestvo, place_of_birth=place_of_birth,
                          place_of_death=place_of_death, date_of_birth=date_of_birth, date_of_death=date_of_death,
                          nationality=nationality, biography=biography, coords=coords,
                          date_of_creation=datetime.now())
        if avatar is not None:
            page.avatar = avatar
        if pictures is not None:
            page.pictures = pictures
        if price is not None:
            page.price = price
        if private is not None:
            page.private = private
        if facts is not None:
            page.facts = facts
        if videos is not None:
            page.videos = videos
        page.qr_code = []
        page.save()
        return page


class Pages(models.Model):
    name = models.CharField('Имя', max_length=20)
    surname = models.CharField('Фамилия', max_length=25)
    otchestvo = models.CharField('Отчество', max_length=25, blank=True)
    place_of_birth = models.CharField('Место рождения', max_length=30, blank=True)
    place_of_death = models.CharField('Место смерти', max_length=30, blank=True)
    date_of_birth = models.DateField('Дата рождения', blank=True, null=True)
    date_of_death = models.DateField('Дата смерти', blank=True, null=True)
    avatar = models.CharField(max_length=70, null=True, blank=True)
    videos = ArrayField(default=list, base_field=models.CharField(max_length=70), blank=True)
    pictures = ArrayField(default=list, base_field=models.CharField(max_length=70), blank=True)
    biography = models.TextField('Биография', max_length=2000, blank=True)
    date_of_creation = models.DateField('Дата создания', null=True)
    payed = models.BooleanField('Оплата', default=False)
    price = models.IntegerField('Цена', default=1390)
    private = models.BooleanField('Скрыта', default=False)
    facts = models.CharField('Факты', max_length=200, blank=True, null=True)
    nationality = models.IntegerField('Национальность', blank=True, default=165)
    coords = ArrayField(null=True, base_field=models.FloatField(), blank=True)
    qr_code = ArrayField(base_field=models.CharField(max_length=70), default=list)
    last_time_opened = models.DateField('Дата создания', null=True, blank=True)

    objects = PagesManager()

    def __str__(self):
        return "{} {}".format(self.name, self.surname)


def upload_path_handler(instance, filename):
    return "users/{id}/{file}.{ext}".format(id=instance.user_id, file=uuid4(), ext=filename.split('.')[-1])


class Files(models.Model):
    user_id = models.IntegerField(null=True)
    file = models.FileField(upload_to=upload_path_handler)


class Nationalities(models.Model):
    country_name = models.CharField(max_length=100)
    img = models.CharField(max_length=10)


class Promocode(models.Model):
    user_id = models.IntegerField(null=True)
    code = models.CharField(max_length=100)
    activation_date = models.DateTimeField('Дата создания', null=True)
