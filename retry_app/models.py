from django.db import models
import re
import bcrypt
from django.contrib import messages


class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name required"
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name should be at least three characters. If your name is shorter, sorry pal."
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name required"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords didn't match"
        return errors
    def login_validator(self,postData):
        errors = {}
        list_of_user_emails = User.objects.filter(email = postData['login_email'])
        if len(list_of_user_emails) == 0:
            errors ['valid_email'] = "email/password does not match"
        else:
            if bcrypt.checkpw(postData['login_password'].encode(),list_of_user_emails[0].password.encode()) == False:
                errors['password_match'] = "email/password does not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length = 100)
    confirm_password = models.CharField(max_length = 100)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class ThoughtManager(models.Manager):
    def new_thought_validator(self,postData):
        errors = {}
        if len(postData['new_desc']) < 5:
            errors['description'] = "Thought should be at least 5 characters."
      
        return errors
class Thought(models.Model):
    description = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, related_name='thoughts', on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User,related_name='liked_thoughts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ThoughtManager()
    