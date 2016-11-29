from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):

    def validate_registration(self, *args):
        print"in validate_registration"
        print"*********"
        print "args:", args
        print"*********"
        first_name=args[0]['ufname']
        last_name=args[0]['ulname']
        alias=args[0]['ualias']
        email=args[0]['uemail']
        password=args[0]['password']
        confirm_pwd=args[0]['confirm_pwd']
        birthdate=args[0]['birth_date']

        print("variables:", first_name, last_name, alias, email, password, confirm_pwd)
        
        errors=[]
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

        if not first_name:
            errors.append("Need to include First Name")
        if not last_name:
            errors.append("Need to include Last Name")             
        if  re.search(r"\d", first_name) or re.search(r"\d", last_name):
            errors.append("Names cannot contain numerals")  
        if not alias:
            errors.append("Need to include an Alias") 
        if not email:
            errors.append("Email cannot be blank!")
        elif not EMAIL_REGEX.match(email):
            errors.append("Invalid Email Address!")
        if not password:
            errors.append("Need to include Password")  
        if not confirm_pwd:
            errors.append("Please Confirm Password")    
        if (len(password) >0 and len(confirm_pwd) >0):
            if password != confirm_pwd:
                errors.append("Password and Confirmation Password does not match") 
            if len(password) < 8:
                 errors.append("Passwords need to contain at least 8 characters") 
        if not birthdate:
            errors.append("Need to include Date of Birth")          

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist: 
            pass
        else:
            errors.append("User with that email ({}) already exists in our database".format(email))
            return(False, errors) 

        if not errors:
            pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print{"********pw_hashed********"}
            print(pw_hashed)
            user = User(first_name=first_name, last_name=last_name, alias=alias, email=email, pw_hash=pw_hashed, birthdate=birthdate)
            user.save()
            user = User.objects.filter(email=email).values() # .values() returns dictionary of elements in list[0]

            
            return(True, user, user[0]['id'])
        else:
            return(False, errors) 

    def validate_login(self, *args):
        errors=[]
        print"in validate_login"
        print"*********"
        print "args:", args
        print"*********"   
        email=args[0]['user_email']
        password=args[0]['password']
       
        try:
            user = User.objects.get(email=email)
            print"try query return for {}:{}".format(email, user)
        except ObjectDoesNotExist:
            errors.append("No such user ({}) exists in our database".format(email))
            print "No such user ({}) exists in our database".format(email)
            return(False, errors) 

        user = User.objects.filter(email=email).values()       
        if bcrypt.hashpw(password.encode(), user[0]['pw_hash'].encode()) == user[0]['pw_hash'].encode():
            print("It Matches!")

            return(True, user[0]['alias'], user[0]['id'] )
        else:
            print("Password Does not Match")
            errors.append("Login failed")
            return(False, errors)  
        

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    birthdate = models.DateField()
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
