from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.context_processors import csrf
from django.contrib.auth.models import User
# from .models import Owner
import time
import os

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


from .models import Owner, Pet, Species, Comment

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

def countComment() :
    count = Comment.objects.all().count()
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
        users = []
        comments = Comment.objects.filter(comment_status = False)
        for comment in comments:
            user = Owner.objects.get(owner_id = comment.owner_id)
            users.append(user)
        return render(request, "user/adminPage.html",{
            "comments" : zip(comments,users)
        })
    else :
        return HttpResponseRedirect(reverse("index"))

def googledrive(file,select):
    file_detail = file.name.split(".")
    print(file_detail)
    mime_type = f'image/{file_detail[1]}'
    if select == "users":
        path = default_storage.save(
        '{}'.format(file),
        ContentFile(file.read()))
        file_medate = {
            'name': file.name,
            'parents':  [folder_users]
        }
    elif select == "pets" :
        path = default_storage.save(
        '{}'.format(file),
        ContentFile(file.read()))
        file_medate = {
            'name': file.name,
            'parents':  [folder_pets]
        }
    media = MediaFileUpload(path, mimetype = mime_type)
    results = service.files().create(
                body=file_medate,
                media_body=media,
                fields='id'
                ).execute()
    print("finish google drive")
    items = results.get('id')
    os.remove('{}'.format(file))
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
        # print(img)
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
            return HttpResponseRedirect(reverse("login"))
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

    pets = Pet.objects.all()
    species = Species.objects.all()
    #pet
    pet_owner = users.owner_pet.all()
    pet_species = []
    pet_profile = []
    for pet in pet_owner :
        pet_img = f'https://drive.google.com/uc?id={pet.pet_profile}'
        pet_profile.append(pet_img)
        pet_spec = []
        for specie in pet.pet_species.all():
            pet_spec.append(specie.species_name)
        # print(pet_spec)
        pet_species.append(pet_spec)
    # if len(pet_owner) == 0:
    #     print("NO PETS")
    # else :
    #     print(pets)

    return render(request, "user/profilePage.html",{
        "type_select" : type_selected,
        "profile": img,
        "pets": zip(pet_owner,pet_species,pet_profile),
        "user": users
    })

def add_pet(request):
    species = Species.objects.all()
    species_select = []
    if request.method == "POST":
        type_pet = request.POST["type_pet"]
        owner_id = request.POST["user"]
        # print(type_pet)
    for specie in species :
        if specie.species_type == type_pet:
            species_select.append(specie.species_name)
    # print(species_select)
    return render(request, "user/petRegister.html", {
        "species": species_select,
        "pet_type": type_pet,
        "ownerId" : owner_id
    })

def petregister(request):
    if request.method == "POST":
        name = request.POST["pet_name"]
        species = request.POST.getlist("species_select")
        hair = request.POST["pet_hair_color"]
        eye = request.POST["pet_eye_color"]
        date = request.POST["birthday"]
        img = request.FILES["pet_profile"] if "pet_profile" in request.FILES else False
        pet_type = request.POST["type_pet"]
        ownerId = request.POST["userId"]
        # print(name, species, hair, eye, date, img, pet_type)
        wdy = str(date).split("-")
        # print(wdy[0], wdy[1], wdy[2])
        if img != False:
            items = googledrive(img,"pets")
            # print(type(items))
            owner = Owner.objects.get(owner_username=request.user.username)
            pet = Pet.objects.create(
                owner_id = ownerId,
                pet_id = countPet(),
                pet_name = name,
                pet_type = pet_type,
                # pet_species = species[0] + _ + species[1],
                pet_hair_color = hair,
                pet_eye_color = eye,
                pet_born_day = wdy[2],
                pet_born_month = wdy[1],
                pet_born_year = wdy[0],
                pet_profile = items
            )
            for specie in species:
                spec = Species.objects.get(species_name = specie)
                pet.pet_species.add(spec)
            owner.owner_pet.add(pet)
            return HttpResponseRedirect(reverse("profile"))
        else :
            return render(request, "user/petRegister.html",{
                "message" : "Picture Failed!"
            })

    return render(request, "user/petRegister.html")

def petdetail(request):
    if request.method == "POST" :
        pet = Pet.objects.get(pet_id=request.POST["petdetail"])
        # owner = request.POST["user"]
    owner_pet = Owner.objects.get(owner_id = pet.owner_id)
    enter_owner = request.user.username
    private = True if owner == enter_owner else False
    pet_img = f'https://drive.google.com/uc?id={pet.pet_profile}'
    owner_img = f'https://drive.google.com/uc?id={owner_pet.owner_profile}'
    pet_spec = []
    for specie in pet.pet_species.all():
        pet_spec.append(specie.species_name)
    gallery = pet.pet_gallery.split(",") if pet.pet_gallery != 'none' else 'none'
    return render(request, "user/petDetail.html",{
        "pet_img" : pet_img,
        "pet" : pet,
        "species" : pet_spec,
        "owner_img" : owner_img,
        "owner" : owner_pet,
        "private" : private,
        "gallery" :gallery
    });

def petedit(request):
    if request.method == "POST" :
        pet = Pet.objects.get(pet_id=request.POST["petedit"])
    pet_profile = f'https://drive.google.com/uc?id={pet.pet_profile}'
    # print(pet_profile)
    species = Species.objects.filter(species_type = pet.pet_type)
    return render(request, "user/petEdit.html",{
        "pet" : pet,
        "species" : species,
        "pet_profile" : pet_profile
    });

def peteditchange(request):
    if request.method == "POST":
        name = request.POST["pet_name"]
        species = request.POST.getlist("species_select")
        hair = request.POST["pet_hair_color"]
        eye = request.POST["pet_eye_color"]
        date = request.POST["birthday"]
        img = request.FILES["pet_profile"] if "pet_profile" in request.FILES else False
        pet_id = request.POST["pet_id"]
        # print(img)
        # print(name, species, hair, eye, date, img, pet_id)
        wdy = str(date).split("-")
        # print(wdy[0], wdy[1], wdy[2])
        pet = Pet.objects.filter(pet_id = pet_id)
        if img != False:
            items = googledrive(img,"pets")
            # print(type(items))
            pet.update(
                pet_profile = items
            )
        pet.update(
            pet_name = name,
            # pet_species = species[0] + _ + species[1],
            pet_hair_color = hair,
            pet_eye_color = eye,
            pet_born_day = wdy[2],
            pet_born_month = wdy[1],
            pet_born_year = wdy[0],
        )

        pet_s = Pet.objects.get(pet_id = pet_id)
        for specie in pet_s.pet_species.all():
            pet_s.pet_species.remove(specie)

        for specie in species:
            spec = Species.objects.get(species_name = specie)
            pet_s.pet_species.add(spec)

        return HttpResponseRedirect(reverse("profile"))

    return render(request, "user/petRegister.html")

def pet(request):
    pets = Pet.objects.all()
    species_pets = []
    profile_pets = []
    owner_name = []
    for pet in pets:
        # print(pet.owner_id)
        if pet.owner_id != "0":
            owner = Owner.objects.get(owner_id = pet.owner_id)
            owner_name.append(owner.owner_name + " " + owner.owner_surname)
            pet_profile = f'https://drive.google.com/uc?id={pet.pet_profile}'
            profile_pets.append(pet_profile)
            pet_spec = []
            for specie in pet.pet_species.all():
                pet_spec.append(specie.species_name)
            species_pets.append(pet_spec)
    return render(request, "user/petPage.html",{
        "pets" : zip(pets,species_pets,profile_pets,owner_name)
    })

def search(request):
    if request.method == "POST" :
        search_input = request.POST["search_input"]
    pet_collect = []
    pet_id = Pet.objects.filter(pet_id__contains=search_input)
    pet_collect.extend(pet_id)
    pet_name = Pet.objects.filter(pet_name__contains=search_input)
    pet_collect.extend(pet_name)
    pet_type = Pet.objects.filter(pet_type__contains=search_input)
    pet_collect.extend(pet_type)
    pets_all = Pet.objects.all()
    pet_species = []
    for pet in pets_all:
        for specie in pet.pet_species.all():
            if search_input in specie.species_name:
                pet_species.append(pet)
    pet_collect.extend(pet_species)

    pets = list(set(pet_collect))
    species_pets = []
    profile_pets = []
    owner_name = []
    for pet in pets:
        # print(pet.owner_id)
        if pet.owner_id != "0":
            owner = Owner.objects.get(owner_id = pet.owner_id)
            owner_name.append(owner.owner_name + " " + owner.owner_surname)
            pet_profile = f'https://drive.google.com/uc?id={pet.pet_profile}'
            profile_pets.append(pet_profile)
            pet_spec = []
            for specie in pet.pet_species.all():
                pet_spec.append(specie.species_name)
            species_pets.append(pet_spec)
    return render(request, "user/petPage.html",{
        "pets" : list(zip(pets,species_pets,profile_pets,owner_name))
    })

def delpet(request):
    if request.method == "POST" :
        pet_id = request.POST["petdelete"]
        # owner = request.POST["user"]
    pet = Pet.objects.filter(pet_id = pet_id)
    pet_s = Pet.objects.get(pet_id = pet_id)
    owner_pet = Owner.objects.get(owner_id = pet_s.owner_id)
    owner_pet.owner_pet.remove(pet_s)
    pet.update(
        owner_id = "0",
        pet_name = "0",
        pet_type = "0",
        pet_hair_color = "0",
        pet_eye_color = "0",
        pet_born_day = "0",
        pet_born_month = "0",
        pet_born_year = "0",
        pet_profile = "0"
    )

    for specie in pet_s.pet_species.all():
        pet_s.pet_species.remove(specie)

    return HttpResponseRedirect(reverse("profile"))

def uploadphoto(request):
    if request.method == "POST":
        pet_id = request.POST["pet_id"]
        img = request.FILES["pet_gallery"] if "pet_gallery" in request.FILES else False
    pet = Pet.objects.filter(pet_id = pet_id)
    petDetail = Pet.objects.get(pet_id = pet_id)
    petGallery = petDetail.pet_gallery
    if img != False:
        items = googledrive(img,"pets")
        photo = f'https://drive.google.com/uc?id={items}'
        # print(type(items))
        if petGallery == 'none':
            pet.update(
                pet_gallery = photo
            )
        else:
            pet.update(
                pet_gallery = petGallery + "," + photo
            )

    return HttpResponseRedirect(reverse("profile"))

def report(request):

    user_id = Owner.objects.get(owner_username = request.user.username).owner_id
    history = Comment.objects.filter(owner_id = user_id)

    return  render(request, "user/reportPage.html",{
        "userId" : user_id,
        "history" : history
    })

def sendrequest(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        detail = request.POST["detail"]

    comment = Comment.objects.create(
        comment_id = countComment(),
        owner_id = user_id,
        comment_detail = detail
    )

    return HttpResponseRedirect(reverse("report"))

def adminconfirm(request):
    if request.method == "POST":
        comment_id = request.POST["comment_id"]

    comment = Comment.objects.filter(comment_id = comment_id)

    comment.update(
        comment_status = True
    )

    return HttpResponseRedirect(reverse("admin"))