from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import random 
import string 



class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    bio = models.TextField(max_length=2000,null=True)
    profile_pic=models.ImageField(default='default.png',upload_to='profile-images')
    gender = models.CharField(max_length=1, choices=GENDER,blank=True)
    slug = models.SlugField(null=True)



    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.profile_pic.path)
    
    def create_slug(size=10, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

class Follwing_count(models.Model):
    follwer = models.CharField(max_length=100)
    follwing = models.CharField(max_length=100)

    def __str__(self):
        return self.follwing

class Agent(models.Model):
    user =   models.OneToOneField(User,on_delete=models.CASCADE)
    agent =  models.CharField(max_length=100)

    def __str__(self) :
        return self.agent