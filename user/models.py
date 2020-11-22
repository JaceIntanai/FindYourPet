from django.db import models

# Create your models here.

class Species(models.Model) :
    species_type = models.CharField(max_length=20)
    species_name = models.CharField(max_length=100)
    # species_name = models.ForeignKey(Pet, related_name='species_name')

    def __str__(self):
        return f"{self.species_type} --> {self.species_name}"


class Pet(models.Model) :
    owner_id = models.CharField(max_length=10, default='0000000')
    pet_id = models.CharField(max_length=10, default='0000000')
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=20)
    pet_species = models.ManyToManyField(Species, blank=True, related_name = "pets")
    pet_hair_color = models.CharField(max_length=100)
    pet_eye_color = models.CharField(max_length=100)
    pet_born_day = models.CharField(max_length=2)
    pet_born_month = models.CharField(max_length=2)
    pet_born_year = models.CharField(max_length=4)
    pet_profile = models.CharField(max_length=300)
    pet_gallery = models.CharField(max_length=100000, default='none')

    def __str__(self):
        return f"{self.owner_id} <= {self.pet_id} {self.pet_name} {self.pet_type} {self.pet_hair_color} {self.pet_eye_color} {self.pet_born_day} {self.pet_born_month} {self.pet_born_year} {self.pet_profile}"

class Owner(models.Model) :
    owner_id = models.CharField(max_length=10, default='0000000')
    owner_username = models.CharField(max_length=64)
    owner_name = models.CharField(max_length=64)
    owner_surname = models.CharField(max_length=64)
    owner_phone = models.CharField(max_length=10)
    owner_email = models.CharField(max_length=64)
    owner_pet = models.ManyToManyField(Pet, blank=True, related_name = "owners")
    owner_profile = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.owner_id} {self.owner_username} {self.owner_name} {self.owner_surname} {self.owner_phone} {self.owner_profile}"

class Comment(models.Model) :
    comment_id = models.CharField(max_length=10, default='0')
    owner_id = models.CharField(max_length=10)
    comment_detail = models.CharField(max_length=10000)
    comment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.comment_id} {self.owner_id} {self.comment_detail} {self.comment_status}"

# class Forum(models.Model) :
#     forum_id = models.CharField(max_length=10)
#     forum_topic = models.CharField(max_length=100)
#     forum_user = models.CharField(max_length=64)
#     forum_comment = models.ManyToManyField(Comment, blank=True, related_name="comments")

#     def __str__(self):
#         return f"{self.forum_id} {self.forum_topic} {self.forum_user}"
