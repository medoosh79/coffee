from django.shortcuts import render ,redirect 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from products.models import Product
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (HttpResponse, render, redirect,
                        get_object_or_404, reverse, get_list_or_404, Http404)

import re

# Create your views here.

def signin(request):
    if request.method == 'POST' and 'btnsignip' in request.POST:
        
        username= request.POST['user']
        password= request.POST['pass']

        user= auth.authenticate(username= username , password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'Welcom in your coffee '  + user.username)
            return redirect('index')
        else:
            messages.error(request, 'username or password invaled')


        return redirect('signin')
    else:
        return render(request, 'accounts/signin.html')


def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:

        # variables for fildes
        fname = None
        lname= None
        address = None
        address2 = None
        city = None
        state = None
        zip = None
        email = None
        username = None
        password = None
        terms= None
        is_added = None

        # Get values from the from
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request , 'Error first name')

        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request , 'Error last name')

        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request , 'Error address')

        if 'address2' in request.POST: address2 = request.POST['address2']
        else: messages.error(request , 'Error address2')

        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request , 'Error city')

        if 'address' in request.POST: address = request.POST['address']
        else: messages.error(request , 'Error address')

        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request , 'Error state')

        if 'zip' in request.POST: zip = request.POST['zip']
        else: messages.error(request , 'Error zip')

        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request , 'Error email')

        if 'user' in request.POST: username = request.POST['user']
        else: messages.error(request , 'Error username')

        if 'pass' in request.POST: password = request.POST['pass']
        else: messages.error(request , 'Error password')

        if 'terms' in request.POST: terms = request.POST['terms']
        

        # Check the values
        if fname and lname and address and address2 and city and state and zip and email and username and password:
            if terms=='on':
                # Check if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is taken')
                else:
                    # Check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This Email is taken')
                    else:
                        patt= '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
                        if re.match(patt, email):
                            # add user
                            user= User.objects.create_user(first_name = fname,last_name = lname, email=email, username= username, password=password )
                            user.save()
                            # add user profile in account table db
                            userprofile = UserProfile(user=user, address = address, address2 = address2 , city= city, state = state, zip = zip)
                            userprofile.save()
                            # Clear fields
                            fname = ''
                            lname= ''
                            address = ''
                            address2 = ''
                            city = ''
                            state = ''
                            zip = ''
                            email = ''
                            username = ''
                            password = ''
                            terms= None

                            # Success Message 
                            messages.success(request, 'Your account has been created')
                            is_added = True
                           
                        else:
                            messages.error(request, 'Invalid email')

            else:
                messages.error(request, 'You must agree to the terms')
        else:
            messages.error(request, 'Check empty fields')

        return render(request, 'accounts/signup.html' , {
                    'fname' : fname,
                    'lname' : lname,
                    'address': address,
                    'address2': address2,
                    'city': city,
                    'state': state,
                    'zip': zip,
                    'email': email,
                    'user':username, 
                    'pass':password,
                    'is_added': is_added,
                })
    else:        
        return render(request, 'accounts/signup.html')

def profile(request):  
    
    if request.method == 'POST' :
        return redirect('profile')    
    else:
        if request.user is not None:
            context=None
            # if request.user.id !=None:
            if not request.user.is_anonymous:
                userprofile= UserProfile.objects.get(user=request.user)
                
                context={
                    'image':userprofile.image,
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'state':userprofile.state,
                    'city':userprofile.city,
                    'zip':userprofile.zip,
                    'mobile':userprofile.mobile,
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password,
                    
                

                }

            return render(request, 'accounts/profile.html', context)
            
        else:
            return redirect('profile')


def profile_edite(request):  
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id !=None:
        
        #if request.user.is_authenticated() and request.user.id == user.id:
            userprofile= UserProfile.objects.get(user= request.user)

            if request.POST['fname'] and request.POST['lname'] and request.POST['address'] and request.POST['address2'] and request.POST['state'] and request.POST['city'] and request.POST['zip'] and request.POST['mobile'] and request.POST['email'] and request.POST['user'] and request.POST['pass'] : #and request.FILES :                         
                
                request.user.first_name= request.POST['fname']
                request.user.last_name= request.POST['lname']
                userprofile.address=request.POST['address']
                userprofile.address2=request.POST['address2']
                userprofile.city=request.POST['city']
                userprofile.state=request.POST['state']
                userprofile.zip=request.POST['zip']
                userprofile.mobile=request.POST['mobile']
                if request.FILES:
                    userprofile.image= request.FILES["image2"]
                
                
                                   
                request.user.save()
                userprofile.save()
                messages.success(request, 'Your date updated')
                return redirect('profile')
            
            else:
                messages.error(request, 'Check your values')

           

        return redirect('profile_edite')    
    else:
        if request.user is not None:
            context=None
            # if request.user.id !=None:
            if not request.user.is_anonymous:
                userprofile= UserProfile.objects.get(user=request.user)
                
                context={
                    'image':userprofile.image,
                    'fname':request.user.first_name,
                    'lname':request.user.last_name,
                    'address':userprofile.address,
                    'address2':userprofile.address2,
                    'state':userprofile.state,
                    'city':userprofile.city,
                    'zip':userprofile.zip,
                    'mobile':userprofile.mobile,
                    'email':request.user.email,
                    'user':request.user.username,
                    'pass':request.user.password,
                    
                

                }

            return render(request, 'accounts/profile_edite.html', context)
            
        else:
            return redirect('profile')

def logout(request):
    logout(request)
    return render(request, 'index.html')


def product_favorite(request, pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_favo = Product.objects.get(pk=pro_id)
        if UserProfile.objects.filter( user=request.user , product_favorites=pro_favo).exists():
            messages.info(request, 'The product is add favorite before')
        else:
            userprofile= UserProfile.objects.get(user= request.user)
            userprofile.product_favorites.add(pro_favo)
            messages.success(request, 'Add favorite Done!')

        return redirect('products' )
    else:
        return redirect('signin')

def show_favorite(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo= UserProfile.objects.get(user=request.user)
        pro= userInfo.product_favorites.all()
        context= {'products':pro}
    return render(request, 'products/products.html', context)