from django.db import models
import re
from time import localtime, strftime
from datetime import datetime



class Usermanager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_address']):    # test whether a field matches the pattern            
            errors['email_address'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = 'passwrd should be at least eight characters'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'passwrod must match'
        if User.objects.filter(email_address = postData['email_address'] ):
            errors['email_address'] = "Account already exists"
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters'
        if len(postData['first_name']) < 2:
            errors['last_name'] = 'first name must be at least 2 characters'
        return errors
    
class Sightingmanager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if int(postData['number']) < 1 :
            errors['number'] = 'Number of Sightings must atleast be 1'
        if len(postData['desc']) > 50 :
            errors['desc'] = "Notes on what happened must not exceed 50 characters"
        if datetime.strptime(postData['date'], "%Y-%m-%d") > datetime.now():
            errors['date'] = 'Time of sighting must be in the past'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email_address = models.CharField(max_length=60)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Usermanager()

class Sighting(models.Model):
    location = models.CharField(max_length=50)
    date = models.CharField(max_length=100)
    number = models.IntegerField()
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_user = models.ForeignKey(User, related_name='suspicius',on_delete=models.CASCADE)
    skeptic = models.ManyToManyField(User, related_name='sightings')
    objects = Sightingmanager()
