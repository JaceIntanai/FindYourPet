from django.test import TestCase, Client
from .models import Species, Pet, Owner, Comment, Forum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.
class FindYourPet_test_case(TestCase):

    def setUp(self):
        # Create owners
        self.owner1 = Owner.objects.create(owner_id="612345"
                                        , owner_username="Reder"
                                        , owner_name="Reder"
                                        , owner_surname="masterred"
                                        , owner_phone="061234567"
                                        , owner_email="red@gg.com"
                                        , owner_profile="../FRONG.jpg")
        self.owner2 = Owner.objects.create(owner_id="678910"
                                        , owner_username="bluer"
                                        , owner_name="bluer"
                                        , owner_surname="masterblue"
                                        , owner_phone="07891011"
                                        , owner_email="blue@gg.com"
                                        , owner_profile="../FRONG.jpg")

        # Create pets
        Pet.objects.create(pet_id="123456"
                        , pet_name="jook"
                        , pet_type="dog"
                        , pet_hair_color="brown"
                        , pet_eye_color="black"
                        , pet_born_day="22"
                        , pet_born_month="9"
                        , pet_born_year="2015"
                        , pet_profile="../FRONG.jpg")

        Pet.objects.create(pet_id="123457"
                        , pet_name="kook"
                        , pet_type="cat"
                        , pet_hair_color="black"
                        , pet_eye_color="blue"
                        , pet_born_day="22"
                        , pet_born_month="9"
                        , pet_born_year="2015"
                        , pet_profile="../FRONG.jpg")
        # Create Users
        self.user1 = User.objects.create_user("6310600000", "6310600000@test.com", "123456")
        self.user2 = User.objects.create_user("6210600001", "6210600001@test.com", "testuser2")
        self.user_admin = User.objects.create_superuser("admin", "admin@admin.admin", "admin")
        # Create Client
        self.client = Client()

    # Redirect
    def redirect(self , res):
        return dict(res.items())['Location']

    # Login page test
    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    # Login test
    def test_login_1(self):
        # with wrong login password
        response = self.client.post('/login', {"username": self.user1.username, "password": "wrong"})
        self.assertEqual(response.context["message"], "Invalid credentials")
        self.assertEqual(response.status_code,200)

    def test_login_2(self):
        # with wrong login username
        response = self.client.post('/login', {"username": "wrong", "password": "testuser1"})
        self.assertEqual(response.context["message"], "Invalid credentials")
        self.assertEqual(response.status_code,200)

    def test_login_3(self):
        user_test = User.objects.filter(email=self.user1.email).first()
        print(user_test)
        user_test.is_active = True
        user_test.save()
        # with correct password
        response = self.client.post('/login', {"username": user_test.username, "password": "123456"})
        # print(self.redirect(response))
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.redirect(response), '/')

    # Logout test
    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.redirect(response), '/login')

    def create_owner(self, oID="test_oID", username="test_username", name="test_name", surname="test_surname", phone="test_surname", email="test_email", profile="test_profile"):
        return Owner.objects.create(owner_id=oID
                                        , owner_username=username
                                        , owner_name=name
                                        , owner_surname=surname
                                        , owner_phone=phone
                                        , owner_email=email
                                        , owner_profile=profile)

    def test_owner_creation(self):
        w = self.create_owner()
        self.assertTrue(isinstance(w, Owner))
        test_w = f"{w.owner_id} {w.owner_username} {w.owner_name} {w.owner_surname} {w.owner_phone} {w.owner_profile}"
        self.assertEqual(w.__str__(), test_w)

    def create_pet(self,pet_id="123457"
                    , pet_name="kook"
                    , pet_type="cat"
                    , pet_hair_color="black"
                    , pet_eye_color="blue"
                    , pet_born_day="22"
                    , pet_born_month="9"
                    , pet_born_year="2015"
                    , pet_profile="../FRONG.jpg"):
        return Pet.objects.create(pet_id=pet_id
                                , pet_name=pet_name
                                , pet_type=pet_type
                                , pet_hair_color=pet_hair_color
                                , pet_eye_color=pet_eye_color
                                , pet_born_day=pet_born_day
                                , pet_born_month=pet_born_month
                                , pet_born_year=pet_born_year
                                , pet_profile=pet_profile)

    def test_pet_creation(self):
        w = self.create_pet()
        self.assertTrue(isinstance(w, Pet))
        test_w = f"{w.pet_id} {w.pet_name} {w.pet_type} {w.pet_hair_color} {w.pet_eye_color} {w.pet_born_day} {w.pet_born_month} {w.pet_born_year} {w.pet_profile}"
        self.assertEqual(w.__str__(), test_w)