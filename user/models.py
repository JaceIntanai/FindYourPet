from django.db import models

# Create your models here.

class Species(models.Model) :
    species_type = models.CharField(max_length=20)
    species_name = models.CharField(max_length=64)


class Pet(models.Model) :
    pet_id = models.CharField(max_length=10)
    pet_name = models.CharField(max_length=64)
    pet_type = models.CharField(max_length=20)
    pet_species = models.ManyToManyField(Species, blank=True, related_name = "pets")
    pet_born_day = models.CharField(max_length=2)
    pet_born_month = models.CharField(max_length=2)
    pet_born_year = models.CharField(max_length=4)


class Owner(models.Model) :
    owner_id = models.CharField(max_length=10)
    owner_username = models.CharField(max_length=10)
    owner_name = models.CharField(max_length=64)
    owner_surname = models.CharField(max_length=64)
    owner_phone = models.CharField(max_length=10)
    owner_pet = models.ManyToManyField(Pet, blank=True, related_name = "owners")

    def __str__(self):
        return f"{self.owner_username} {self.owner_name} {self.owner_surname} {self.owner_phone}"

class Comment(models.Model) :
    comment_id = models.CharField(max_length=10)
    comment_detail = models.CharField(max_length=300)

class Forum(models.Model) :
    forum_id = models.CharField(max_length=10)
    forum_topic = models.CharField(max_length=100)
    forum_user = models.CharField(max_length=64)
    forum_comment = models.ManyToManyField(Comment, blank=True, related_name="comments")

