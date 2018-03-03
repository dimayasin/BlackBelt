# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt
import datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z+ ]+$')
USER_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')


class UsersManager(models.Manager):
    def validateRegistrationData(self, postData):
        errors = []
        mytime=datetime.datetime.strptime(postData['dob'], '%Y-%m-%d').date()
        time2 = datetime.datetime.today().date()
        if len(postData['name']) < 2:
            errors.append("User name should be more than 2 characters")
        if not NAME_REGEX.match(postData["name"]):
            errors.append( "User name should contain letters only!")
        if mytime >= time2 :
            errors.append("Birth date shouldn't be a current or future date.")
        
        
        if  not EMAIL_REGEX.match(postData['email']) or not re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",postData['email']):
            errors.append( "Invalid Email Address.")
        if len(postData['psswrd']) < 8:
            errors.append( "User password should be more than 8 characters")
        if not postData['psswrd'] == postData['cpsswrd']:
            errors.append( "User passwords do not match.")
        test = Users.objects.filter(email = postData['email'])
        if test :
            errors.append( "Email already exists.")


        return errors

    def validateLoginData(self, postData):
        errors = []
        if not postData['email']:
            errors.append("Email is needed for login.")
        if not postData['psswrd']:
            errors.append("Password is needed for login.")
        if Users.objects.filter(email = postData['email']):
            obj= Users.objects.get(email = postData['email'])
            temp=obj.password
            if not bcrypt.checkpw(postData['psswrd'].encode(),temp.encode()):
                errors.append("Invalid Password")
        else:
            errors.append( "There is no registered email address")

        if not re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",postData['email']):
            errors.append("User email has the wrong format.")
        if len(postData['psswrd']) < 8:
            errors.append( "User password should be more than 8 characters")

        return errors

class QuotesManager(models.Manager):
    def ValidateQuotes(self, postData):
        errors=[]
        if not postData['myquote'] or not postData['msg']:
            errors.append("All field should have values.")  
        if len(postData['myquote']) <= 3:
            errors.append("Quoted by field should be more than 3 characters")
        if len(postData['msg']) <= 10:
            errors.append("Your quote should be more than 10 characters")
 
        return errors
    
class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    DOB=models.DateField(default= datetime.date.today)
    objects = UsersManager()

class Quotes(models.Model):
    quoted_by = models.CharField(max_length=255)
    favorites = models.BooleanField(default = False)
    msg = models.CharField(max_length=500)
    quoted = models.ManyToManyField(Users,related_name="quoted_by")
    posted_by = models.ForeignKey(Users, related_name="posted_by")
    objects = QuotesManager()