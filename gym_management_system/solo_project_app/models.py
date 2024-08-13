from django.db import models
import re
from datetime import datetime

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not (postData.get('first_name') and postData.get('last_name') and postData.get('email')):
            errors["fields"] = "All fields must be present"
        
        if len(postData.get('first_name', '')) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData.get('last_name', '')) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        # if postData.get('age', '') < 12 :
        #     errors["age"] = "User must be at least 12 years old"
        if len(postData.get('phone_number', '')) != 10 :
            errors["phone_number"] = "Phone number invalid"
        email = postData.get('email','');
        if User.objects.filter(email=email).exists():
            errors['unique', ''] = "This email address is already used"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = "Invalid email address!"
        # if len(postData.get('password', '')) < 8:
        #     errors["password"] = "Password should be at least 8 characters"
        # if postData.get('confirm_password', '') != postData.get('password', '') :
        #     errors["confirm_password"] = "Both passwords must be identical!"
        return errors
    
class ClassManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not (postData.get('title')):
            errors["title"] = "title must be present"
        if not (postData.get('description')):
            errors["description"] = "Please Include the description"
        if not (postData.get('max_size')):
            errors["crust"] = "Please Include the maximum size"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dateofbirth = models.DateField(blank = True, null = True)
    phone_number = models.IntegerField()
    email = models.CharField(max_length=255)
    medical_history = models.TextField(blank=True,null=True)
    address = models.CharField(max_length=255 ,blank = True, null = True)
    password = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Class(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    max_size = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, related_name="classes")
    objects = ClassManager()

class Specialty(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="specialties", on_delete=models.CASCADE)

class Subscription(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="subscriptions", on_delete=models.CASCADE)


class Role(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="roles", on_delete=models.CASCADE , blank =True,null = True)

class AdminManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        username = postData.get('username', '')
        password = postData.get('password', '')
        
        if not (username and password):
            errors["fields"] = "All fields must be present"
        elif username != 'admin' or password != 'admin123':
            errors["credentials"] = "Invalid username or password."
        
        return errors
    
class Admin(models.Model):
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()

