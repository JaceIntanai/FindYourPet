from django.contrib import admin

from .models import Species, Pet, Owner
# Register your models here.

admin.site.register(Species)
admin.site.register(Pet)
admin.site.register(Owner)