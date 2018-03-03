# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
import bcrypt
from .models import Users
from .models import Quotes


import datetime

secret_key = 'TARDIS' 
context ={}

# Create your views here.
def index(request):
    users = Users.objects.all()
    # errors = []

    request.session['id']=5
    request.session['quote'] = 0
    request.session['fav'] = []

    context ={
        'users': users
    }
    return render(request, "index.html",context)


def log(request):
    return render(request,"login.html")


def logins(request):
    errors = Users.objects.validateLoginData(request.POST)
    if len(errors)>0:
        for error in errors:
            messages.error(request,error)
        return render(request,"login.html")
    else:
 
        users = Users.objects.filter(email = request.POST['email'])[0]
        request.session['id'] = users.id
        request.session['name'] = users.name 

        context={
            'users': users
        }
        return redirect("/show", context)

def new_user(request):
    return render(request,"registration.html")

def Registration(request):
    errors = Users.objects.validateRegistrationData(request.POST)
    if len(errors)>0:
        for error in errors:
            messages.error(request,error)
        return render(request,"registration.html")
    else:
        hasher1 = bcrypt.hashpw(request.POST['psswrd'].encode(), bcrypt.gensalt())
        Users.objects.create( 
            name=request.POST['name'],
            email=request.POST['email'], 
            password=hasher1, 
            # DOB= datetime.datetime.strptime(request.POST['DOB'], '%Y-%m-%d')
            # DOB= request.POST['DOB']

            )
        users = Users.objects.filter(email = request.POST['email'])[0]
        context={
            'users': users
        }
        request.session['id'] = users.id
        request.session['name'] = users.name 

        return redirect("/show", context)

def new_quote(request):
    return render(request,"new_quote.html")

def additem(request):
    errors = Quotes.objects.ValidateQuotes(request.POST)


    if len (errors)>0:
        for error in errors:   
            messages.error(request,error)
        return render(request,"new_quote.html")

    else:
        user = Users.objects.get(id = request.session['id'])
        Quotes.objects.create( 
            quoted_by=request.POST['myquote'],
            msg= request.POST['msg'], 
            posted_by= user
        )
        
        quote = Quotes.objects.filter()
        request.session['id'] = user.id
        request.session['name'] = user.name
        context={
            'quotes': quote
        }
        return redirect("/show", context)



def show(request):
    # show_quotes = Quotes.objects.filter()
    # myfav=[]
    # notfav=[]
    # for myquote in show_quotes:
    #     if myquote.favorites == True:
    #         myfav += Quotes.objects.filter(id=myquote.id)
    #     else:
    #         notfav +=Quotes.objects.filter(id=myquote.id)
    

    # context={
    #         'no_faves' : notfav,
    #         "favorites":myfav 
    #     }
        
    user = Users.objects.filter(id=request.session['id'])[0]
    show_list = Quotes.objects.filter(posted_by = user)
    favelist= Quotes.objects.filter(quoted = user)
    not_fav_list = Quotes.objects.exclude(posted_by = user).exclude(quoted= user)



    context={
            'this_quotelist' : show_list,
            'nofaves':not_fav_list ,
            'favelists':favelist
        }
    
 
 
    return render(request, "quotes.html", context)


def user_quotes(request,id):
    user=Users.objects.filter(id=id)
    quote = Quotes.objects.filter(posted_by=user)
    count=len(quote)
    context={
        'quotes': quote,
        'count':count
    }
    return render(request,"user_quotes.html",context)


def favorites(request, id):
    user = Users.objects.get(name=request.session['name'])

    myfav = Quotes.objects.get(id=id)

    myfav.quoted.add( user)
    myfav.save()

    return redirect("/show")


def notfavorite(request, id):
    user = Users.objects.get(name=request.session['name'])

    myfav = Quotes.objects.get(id=id)

    myfav.quoted.remove( user)
    myfav.save()

    return redirect("/show")

def out(request):
    request.session.clear()
    return redirect ("/log")


def showlist(request,id):
    user_quote = Users.objects.get(id=id)
    name = user_quote.name
  
    myquote = Quotes.objects.filter(posted_by=user_quote)
    
   
    msgs=[]
    for q in myquote:
        msgs.append(q.msg)
    count = len(msgs)
    context = {
        'quotes':myquote,
        'msgs':msgs,
        'count':count,
        'name' : name
    }


    return render(request,"user_quotes.html", context)
