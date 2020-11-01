from django.contrib import admin

from .models import Species, Pet, Owner
# Register your models here.

class Owner_list(admin.ModelAdmin):
    list_display = ("owner_id", "owner_username", "owner_name", "owner_surname", "owner_phone", "owner_email","owner_profile")

class Pet_list(admin.ModelAdmin):
    list_display = ("pet_id", "pet_name", "pet_type", "pet_hair_color", "pet_eye_color", "pet_born_day","pet_born_month","pet_born_year","pet_profile")

class Species_list(admin.ModelAdmin):
    list_display = ("species_type","species_name")


admin.site.register(Species,Species_list)
admin.site.register(Pet,Pet_list)
admin.site.register(Owner,Owner_list)