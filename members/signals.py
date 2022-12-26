from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import string ,random
from unidecode import unidecode
from django.template.defaultfilters import slugify

from .models import Profile
#this signal will create the profile when a new user is registered
def create_profile(sender, instance, created, **kwargs):
    if created:
        char = string.ascii_lowercase
        size = 10
        letters = instance.username+''.join(random.choice(char) for _ in range(size))
        slug = slugify(unidecode(letters))
        Profile.objects.create(user=instance,slug=slug)
        print("The profile is successfully created!")
#this signal will trigger to create the profile when a new user is registered     
post_save.connect(create_profile,sender=User)