from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name='about'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('ownregister', views.ownregister, name='ownregister'),
    path('admin', views.admin, name='admin'),
    path('profile', views.profile, name='profile'),
    path('addpet', views.add_pet, name='addpet'),
    path('petregister', views.petregister, name='petregister'),
    path('petdetail', views.petdetail, name='petdetail'),
    path('petedit', views.petedit, name='petedit'),
    path('peteditchange', views.peteditchange, name='peteditchange'),
    path('pet', views.pet, name="pet")
]