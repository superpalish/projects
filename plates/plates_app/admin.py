from django.contrib import admin

# Register your models here.
from plates_app.models import NumberPlate, Owner, PersonId

admin.site.register(NumberPlate)
admin.site.register(Owner)
admin.site.register(PersonId)