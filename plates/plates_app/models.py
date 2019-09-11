# coding: utf-8
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


class PersonId(models.Model):
    PASSPORT = 'PT'
    DRIVER_LISENCE = 'DL'
    DELETED = 'DEL'
    TYPES = [
        (PASSPORT, 'PASSPORT'),
        (DRIVER_LISENCE, 'DRIVER_LISENCE'),
        (DELETED, 'DELETED')
    ]

    id_type = models.CharField(choices=TYPES, max_length=100)
    value = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return "%s %s" % (dict(self.TYPES)[self.id_type], self.value)


class Owner(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    document = models.OneToOneField('PersonId',
                                    on_delete=models.PROTECT,
                                    )
    plates = models.ForeignKey('NumberPlate', on_delete=models.SET_NULL, null=True, related_name='owners')

    def full_name(self):
        return "{} {} {}".format(self.last_name, self.first_name, self.middle_name)

    def __str__(self):
        return self.full_name()


class NumberPlate(models.Model):
    plates_number = models.CharField(max_length=12, validators=[
        RegexValidator(
            regex='^\w{1}\d{3}\w{2}\d{2,3}rus',
            message='Format does not comply. ex. а888тт88rus ',
        ),
    ])
    car_model = models.CharField(max_length=250)
    model_image = models.ImageField('Car model image', upload_to='model_images', blank=True)

    def __str__(self):
        return self.plates_number
