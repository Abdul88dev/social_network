from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Profile ,Follwing_count
from django.views.generic import DetailView ,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from unidecode import unidecode
from django.template.defaultfilters import slugify
import string ,random
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, 'You Are already signed in')
        return redirect('/')
    else:
        if request.method =="POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                
                return redirect('/')
            else :
                messages.add_message(request, messages.INFO, 'There was a problem loging in Try Again')
                return render(request,'members/login.html',{})
        else :
            return render(request,'members/login.html',{})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.INFO, 'You Are Signed out or Not Registered')
        return redirect('/')
    else:
        return redirect('/')


def register_user(request):
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            email    = request.POST["email"]
            user_exist = False
            try:
                User.objects.get(username=username)
                user_exist = True
            except:
                pass
            if not user_exist:
                user=User.objects.create_user(username=username,password=password,email=email)
                #char = string.ascii_lowercase
                #size = 10
                #letters = username+''.join(random.choice(char) for _ in range(size))
                #slug = slugify(unidecode(letters))
                #Profile.objects.create(user=user,slug=slug)
                login(request,user)
                return redirect('/')
            else :
                return render(request,'members/register.html',{})
        elif request.method == 'GET': 
            return render(request, 'members/register.html', {})

class UserProfile(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'members/profile.html'
    

class UserProfiles(DetailView):
    model= Profile
    template_name = 'members/profile.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        userobject = get_object_or_404(Profile, slug=self.kwargs['slug'])
        if Follwing_count.objects.filter(follwer=self.request.user.username,follwing=userobject.user.username):
            button_text = "Unfollow"
        else:
             button_text = "Follow"
        followers=Follwing_count.objects.filter(follwer=userobject.user)
        followers_count = Follwing_count.objects.filter(follwing=userobject.user)
        data['following'] = len(followers)
        data['followers'] = len(followers_count)
        data['button_text'] = button_text
        return data
    

def follwingview(request):
    if request.method == 'POST':
        follower = request.POST['follwer']
        following = request.POST['following']
        following_id = request.POST['follwingid']
        slug = Profile.objects.get(user=following_id)

        if Follwing_count.objects.filter(follwer=follower, follwing=following).first():
            delete_follower = Follwing_count.objects.get(follwer=follower, follwing=following)
            delete_follower.delete()
            return redirect('profile/'+slug.slug)
        else:
            new_follower = Follwing_count.objects.create(follwer=follower, follwing=following)
            new_follower.save()
            return redirect('profile/'+slug.slug)
    else:
        return redirect('/')



