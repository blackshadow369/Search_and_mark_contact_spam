from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout,login
from spamapp.models import Information
from django.contrib.auth.hashers import make_password,check_password

# Page for the registrations of the users
def spamapp_signup(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        password1 = request.POST.get('pwd1')
        password2 = request.POST.get('pwd2')
        number_len = len(request.POST.get('number'))
        number = int(request.POST.get('number'))

        #redirect again to registration page if passwords not match
        if password1!=password2:
            messages.error(request,'both password did not match. Fill again')
            return redirect('/')
        elif number_len!=10: #only take number if it exactly 10 digit
            messages.error(request,'please enter valid number')
            return redirect('/')
        elif numberused(number) == True: #check if the number has been used for creating a account or not
             messages.error(request,'Number has already been used.')
             return redirect('/')
        else: # if the email exist
            if request.POST['email']:
                pwd = make_password(password1)
                my_user = Information.objects.create(Information_name=uname,
                                                     Information_password=pwd,
                                                     Information_phone=number,
                                                     Information_email=request.POST['email'],
                                                     Information_used=True)
                my_user.save()
            else: # if email not exist
                pwd = make_password(password1)
                my_user = Information.objects.create(Information_name=uname,
                                                     Information_password=pwd,
                                                     Information_phone=number,
                                                     Information_used=True)
                my_user.save()
            return redirect('searchbar')
    return render(request,"signup.html")

# to check manually name and the hased password in the database
def self_auth(name,password):
    try:
        a = Information.objects.filter(Information_name=name)
        for value in a:
                    if check_password(password,value.Information_password) == True:
                        print("It is a match")
                        return True
        return False
    except:
         print("Empty")
         return False

# function to check whether the number has been already used or not.
def numberused(number:int):
        record = Information.objects.filter(Information_phone=number)
        try: 
            return record[0].Information_used
        except:
             return False
    


# login page 
def spamapp_login(request):
    if request.method == 'POST':
         if self_auth(request.POST.get('uname'),request.POST.get('pwd')) :
              return redirect('searchbar')
         else:
              messages.error(request,'Wrong credentials Input.Try again.')
              return redirect('login')
         
    return render(request,"login.html")

# a approach so that user cannot direct access the searchbar url without login
def get_referer(request):
     referer = request.META.get('HTTP_REFERER')
     if not referer:
          return None
     return referer     

# searchbar page
def spamapp_searchbar(request):
        data = {}
        value = ""
        if not get_referer(request):
             return redirect('login')
        if request.method == "POST":
            try: 
                number = int(request.POST.get('value'))
                value = str(number)
                data = Information.objects.filter(Information_phone__icontains=number)
            except:   
                strng = request.POST.get('value')
                value = strng
                data = Information.objects.filter(Information_name__icontains=strng)
        return render(request,"searchbar.html",{'data':data,'value':value})

# function to add a number from searchbar (this function will only trigger if number is 10 digits exactly) 
def spamapp_addnumber(request,value):
     value = int(value)
     messages.error(request,'Number successfully added to the database')
     myuser = Information.objects.create(Information_phone=value)
     myuser.save()
     return redirect('searchbar')

# function to increment the spammer number with the help of its id
def spamapp_incspam(request,id):
    temp = Information.objects.get(id=id)
    value = temp.Information_spam
    value = value +1
    temp.Information_spam = value
    temp.save()
    messages.error(request,'Scam account increased.Thank you for help.')
    return redirect('searchbar')  

#function to add name of a number if the name of number is anonymous
def spamapp_addname(request,id):

    if request.method == "POST":
         temp = Information.objects.get(id=id)
         temp.Information_name = request.POST.get('name')
         temp.save()
         messages.error(request,'Name successfully added to the database')
         return redirect('searchbar')     
    return render(request,"addname.html",{'id':id})