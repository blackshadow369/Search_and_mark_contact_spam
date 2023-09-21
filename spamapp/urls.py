from django.contrib import admin
from django.urls import path,include
from spamapp import views

urlpatterns = [
    path('',views.spamapp_signup,name = "signup"), #signup page
    path('searchbar/',views.spamapp_searchbar,name = "searchbar"), #searchbar page
    path('login/',views.spamapp_login,name='login'), #login page
    path('addnumber/<int:value>',views.spamapp_addnumber,name="addnumber"), #addnubmer function
    path('incspam/<int:id>',views.spamapp_incspam), #increment spam number function 
    path('addname/<int:id>',views.spamapp_addname,name="addname"), #addname function 
]