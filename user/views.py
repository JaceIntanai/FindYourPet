from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from .models import Owner
import time

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from googleapiclient.http import MediaFileUpload

# Connect google drive api

from Google import Create_Service
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPE = ['https://www.googleapis.com/auth/drive']

folder_users = '1HctLHzCqoKy12FHWa0N0V0BlKQQ1AUfG'
folder_pets = '1TPurKMay_uIlUCw80tclRhs75gSZS6IW'

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)


from .models import Owner, Pet, Species

# Create your views here.
def owner(request):
	args = {}
	args.update(csrf(request))
	args['owner'] = Owner.objects.all()
	return render('index.html', args)

def countUser() :
    count = Owner.objects.all().count()
    return str(count + 1)

def countPet() :
    count = Pet.objects.all().count()
    return str(count + 1)

def about(request) :
    return render(request, "user/about.html")

def index(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else :
        if not request.user.is_staff:
            return render(request, "user/homePage.html")
        else:
            return HttpResponseRedirect(reverse("admin"))

def login_view(request):
    if request.user.is_authenticated :
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse("index"))
        else :
            return HttpResponseRedirect(reverse("admin"))
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    print("admin")
                    return HttpResponseRedirect(reverse("admin"))
                else:
                    print("user")
                    return HttpResponseRedirect(reverse("index"))
            else:
                print("invalid")
                return render(request, "user/loginPage.html", {
                    "message" : "Invalid credentials"
                })
        print("out of post")
        return render(request, "user/loginPage.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def admin(request):
    if request.user.is_staff:
        return render(request, "user/adminPage.html")
    else :
        return HttpResponseRedirect(reverse("index"))

def googledrive(file,select):
    print(file.name)
    mime_type = 'image/jpeg'
    if select == "users":
        path = default_storage.save(
        '/home/ubuntu/FindYourPet/user/storage/users/{}'.format(file),
        ContentFile(file.read()))
        file_medate = {
            'name': file.name,
            'parents':  [folder_users]
        }
    else :
        path = default_storage.save(
        '/home/ubuntu/FindYourPet/user/storage/pets/{}'.format(file),
        ContentFile(file.read()))
        file_medate = {
            'name': file,
            'parents':  [folder_pets]
        }
    media = MediaFileUpload(path, mimetype = mime_type)
    results = service.files().create(
                body=file_medate,
                media_body=media,
                fields='id'
                ).execute()
    print("next")
    items = results.get('id')
    return items

def ownregister(request):
    if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]
            name = request.POST["name"]
            surname = request.POST["surname"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            img = request.FILES["profile"] if "profile" in request.FILES else False
            print(img)
            users = Owner.objects.filter(owner_username = username)
            if password != confirm_password :
                return render(request, "user/ownRegister.html",{
                    "message" : "Not same password!"
                })
            if img == False :
                return render(request, "user/ownRegister.html",{
                    "message" : "Choose your picture!"
                })
            if not users and img != False:
                items = googledrive(img,"users")
                User.objects.create_user(
                    username = username,
                    password = password,
                    email = email,
                    first_name = name,
                    last_name = surname
                )
                Owner.objects.create(
                    owner_profile = items,
                    owner_id = countUser(),
                    owner_username = username,
                    owner_name = name,
                    owner_surname = surname,
                    owner_phone = phone,
                    owner_email = email
                )
                return render(request, "user/loginPage.html",{
                    "message" : "Register Success!"
                })
            else :
                return render(request, "user/ownRegister.html",{
                    "message" : "Username already used!"
                })

    return render(request, "user/ownRegister.html")

def profile(request):
    users = Owner.objects.get(owner_username = request.user.username)
    type_selected = ["dog", "cat"]
    # print(users.owner_name)
    img = f'https://drive.google.com/uc?id={users.owner_profile}'
    return render(request, "user/profilePage.html",{
        "user": users,
        "type_select" : type_selected,
        "profile": img
    })

def add_pet(request):
    species = Species.objects.all()
    species_select = []
    if request.method == "POST":
        type_pet = request.POST["type_pet"]
        # print(type_pet)
    for specie in species :
        if specie.species_type == type_pet:
            species_select.append(specie.species_name)
    # print(species_select)
    return render(request, "user/petRegister.html", {
        "species": species_select,
        "pet_type": type_pet
    })

def petregister(request):
    if request.method == "POST":
        name = request.POST["pet_name"]
        species = request.POST["species_select"]
        hair = request.POST["pet_hair_color"]
        eye = request.POST["pet_eye_color"]
        date = request.POST["birthday"]
        img = request.FILES["pet_profile"] if "pet_profile" in request.FILES else False
        print(species, date)
        # users = Owner.objects.filter(owner_username = username)
        # if password != confirm_password :
        #     return render(request, "user/ownRegister.html",{
        #         "message" : "Not same password!"
        #     })
        # if img == False :
        #     return render(request, "user/ownRegister.html",{
        #         "message" : "Choose your picture!"
        #     })
        # if not users and img != False:
        #     items = googledrive(img,"pets")
        #     User.objects.create_user(
        #         username = username,
        #         password = password,
        #         email = email,
        #         first_name = name,
        #         last_name = surname
        #     )
        #     Owner.objects.create(
        #         owner_profile = items,
        #         owner_id = countUser(),
        #         owner_username = username,
        #         owner_name = name,
        #         owner_surname = surname,
        #         owner_phone = phone,
        #         owner_email = email
        #     )
    #         return render(request, "user/loginPage.html",{
    #             "message" : "Register Success!"
    #         })
    #     else :
    #         return render(request, "user/ownRegister.html",{
    #             "message" : "Username already used!"
    #         })

    # return render(request, "user/ownRegister.html")