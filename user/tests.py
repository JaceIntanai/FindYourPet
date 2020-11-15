from django.test import TestCase, Client
from .models import Species, Pet, Owner, Comment, Forum
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import tempfile

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
        # self.owner2 = Owner.objects.create(owner_id="678910"
        #                                 , owner_username="bluer"
        #                                 , owner_name="bluer"
        #                                 , owner_surname="masterblue"
        #                                 , owner_phone="07891011"
        #                                 , owner_email="blue@gg.com"
        #                                 , owner_profile="../FRONG.jpg")

        # Create pets
        self.pet1 = Pet.objects.create(pet_id="123456"
                                        , pet_name="jook"
                                        , pet_type="dog"
                                        , pet_hair_color="brown"
                                        , pet_eye_color="black"
                                        , pet_born_day="22"
                                        , pet_born_month="9"
                                        , pet_born_year="2015"
                                        , pet_profile="../FRONG.jpg")
        # self.species = Species.objects.create(species_type="dog1", species_name="shiwawa")
        # self.comment = Comment.objects.create(comment_id="567891", comment_detail="Wow, so cute!")
        # self.forum = Forum.objects.create(forum_id="8521472", forum_topic="My pet is missing", forum_user="Reder")
        # Pet.objects.create(pet_id="123457"
        #                 , pet_name="kook"
        #                 , pet_type="cat"
        #                 , pet_hair_color="black"
        #                 , pet_eye_color="blue"
        #                 , pet_born_day="22"
        #                 , pet_born_month="9"
        #                 , pet_born_year="2015"
        #                 , pet_profile="../FRONG.jpg")
        # Create Users
        self.user1 = User.objects.create_user("6310600000", "6310600000@test.com", "123456")
        self.user2 = User.objects.create_user("6210600001", "6210600001@test.com", "testuser2")
        self.user3 = User.objects.create_superuser("admin", "admin@admin.admin", "admin")
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
        # with correct password
        user_test = User.objects.filter(email=self.user1.email).first()
        user_test.is_active = True
        user_test.save()
        response = self.client.post('/login', {"username": user_test.username, "password": "123456"})
        self.assertEqual(response.status_code,302)
        self.assertEqual(self.redirect(response), '/')


    # Logout test
    def test_logout(self):
        # logout after login
        self.client.force_login(self.user1)
        response = self.client.post('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.redirect(response), "/login")
    # Test owner register
    def test_owner_register(self):
        # register not upload image
        response = self.client.post('/ownregister',{'username':'6010610003',
                                                    'name':'student',
                                                    'surname':'student',
                                                    'password':'',
                                                    'confirm_password':'',
                                                    'email':'dasda@gmail.com',
                                                    'phone':'0123456',
                                                    'profile':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'user/ownRegister.html')
        self.assertEqual(response.context["message"],"Choose your picture!")

    def test_owner_register_1(self):
        # register password not the same as confirm password
        response = self.client.post('/ownregister',{'username':'6010610003',
                                                    'name':'student',
                                                    'surname':'student',
                                                    'password':'1',
                                                    'confirm_password':'',
                                                    'email':'dasda@gmail.com',
                                                    'phone':'0123456',
                                                    'profile':''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'user/ownRegister.html')
        self.assertEqual(response.context["message"],"Not same password!")


    def test_owner_register_2(self):
        # user name was used
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            response = self.client.post('/ownregister',{'username':'Reder',
                                                        'name':'Reder',
                                                        'surname':'student',
                                                        'password':'',
                                                        'confirm_password':'',
                                                        'email':'dasda@gmail.com',
                                                        'phone':'0123456',
                                                        'profile': data})
            self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'user/ownRegister.html')
        self.assertEqual(response.context["message"],"Username already used!")

    # Test pet register
    def test_pet_register(self):
        # pet registeration with no imgae upload
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        with open(tmp_file.name, 'rb') as data:
            response = self.client.post('/petregister',{'pet_name':'coco',
                                                        'species_select':'golden',
                                                        'pet_hair_color':'brown',
                                                        'pet_eye_color':'blue',
                                                        'birthday':'dasda@gmail.com',
                                                        'pet_profile': '',
                                                        'type_pet':'dog',
                                                        'userId':'123456'})
            self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'user/petRegister.html')
        self.assertEqual(response.context["message"],"Picture Failed!")

    # Model test
    @classmethod
    def setUpTestData(cls):
        cls.owner = Owner.objects.create(
            owner_id="test_oID"
            , owner_username="test_username"
            , owner_name="test_name"
            , owner_surname="test_surname"
            , owner_phone="test_phone"
            , owner_email="test_email"
            , owner_profile="test_profile"
        )
        cls.pet = Pet.objects.create(
            owner_id="552548"
            ,pet_id="123457"
            , pet_name="kook"
            , pet_type="cat"
            , pet_hair_color="black"
            , pet_eye_color="blue"
            , pet_born_day="22"
            , pet_born_month="9"
            , pet_born_year="2015"
            , pet_profile="../FRONG.jpg"
        )
        cls.forum = Forum.objects.create(
            forum_id="852147"
            , forum_topic="My pet is missing"
            , forum_user="Reder"
        )

    def test_comment_can_be_attached_to_multiple_forum(self):
        comments = [Comment.objects.create() for _ in range(8)]
        for comment in comments:
            comment.comments.add(self.forum)
        self.assertEquals(len(comments), self.forum.forum_comment.count())
        for comment in comments:
            self.assertIn(comment, self.forum.forum_comment.all())

    def test_owner_can_be_attached_to_multiple_pet(self):
        pets = [Pet.objects.create() for _ in range(8)]
        for pet in pets:
            pet.owners.add(self.owner)
        self.assertEquals(len(pets), self.owner.owner_pet.count())
        for pet in pets:
            self.assertIn(pet, self.owner.owner_pet.all())

    def test_pet_can_be_attached_to_multiple_species(self):
        species = [Species.objects.create() for _ in range(11)]
        for specy in species:
            specy.pets.add(self.pet)
        self.assertEquals(len(species), self.pet.pet_species.count())
        for specy in species:
            self.assertIn(specy, self.pet.pet_species.all())

    def create_owner(self, oID="test_oID", username="test_username", name="test_name", surname="test_surname", phone="test_phone", email="test_email", profile="test_profile"):
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

    def create_pet(self, owner_id="552548"
                    ,pet_id="123457"
                    , pet_name="kook"
                    , pet_type="cat"
                    , pet_hair_color="black"
                    , pet_eye_color="blue"
                    , pet_born_day="22"
                    , pet_born_month="9"
                    , pet_born_year="2015"
                    , pet_profile="../FRONG.jpg"):
        return Pet.objects.create(owner_id=owner_id
                                ,pet_id=pet_id
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
        test_w = f"{w.owner_id} <= {w.pet_id} {w.pet_name} {w.pet_type} {w.pet_hair_color} {w.pet_eye_color} {w.pet_born_day} {w.pet_born_month} {w.pet_born_year} {w.pet_profile}"
        self.assertEqual(w.__str__(), test_w)

    def create_species(self, species_type="dog", species_name="shiba"):
        return Species.objects.create(species_type=species_type, species_name=species_name)

    def test_species_creation(self):
        w = self.create_species()
        self.assertTrue(isinstance(w, Species))
        test_w = f"{w.species_type} --> {w.species_name}"
        self.assertEqual(w.__str__(), test_w)

    def create_comment(self, comment_id="56789", comment_detail="Wow, so cute"):
        return Comment.objects.create(comment_id=comment_id, comment_detail=comment_detail)

    def test_create_comment(self):
        w = self.create_comment()
        self.assertTrue(isinstance(w, Comment))
        test_w = f"{w.comment_id} {w.comment_detail}"
        self.assertEqual(w.__str__(), test_w)

    def create_forum(self, forum_id="852147", forum_topic="My pet is missing", forum_user="Reder"):
        return Forum.objects.create(forum_id=forum_id, forum_topic=forum_topic, forum_user=forum_user)

    def test_create_forum(self):
        w = self.create_forum()
        self.assertTrue(isinstance(w, Forum))
        test_w = f"{w.forum_id} {w.forum_topic} {w.forum_user}"
        self.assertEqual(w.__str__(), test_w)
