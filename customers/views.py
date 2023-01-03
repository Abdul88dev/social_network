from django.views import View
from django.urls import reverse ,reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django_user_agents.utils import get_user_agent
from django.http import JsonResponse
from django.core import serializers

from .models import Post,Comment 
from members.models import Profile,Follwing_count
from .forms import CommentForm,CreateForm
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
# Create your views here.

class Mainview(OwnerListView):
    model=Post
    template_name='customers/index.html'

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            posts=Post.objects.all().order_by('-created_at')
            profiles=Profile.objects.all()
            #getting the user browser info
            user_agent = get_user_agent(request).browser.family
            #passing the create form to the main page
            create_form = CreateForm()

            followers_posts_list = {}
            try:
                userobject = get_object_or_404(Profile, user=self.request.user)
                followers=Follwing_count.objects.filter(follwer=userobject.user)
                following = len(Follwing_count.objects.filter(follwing=userobject.user))
                follower_count = len(followers)
                for follower in followers :
                    user_object = User.objects.get(username=follower)
                    followers_posts_list=Post.objects.filter(owner=user_object)
            except:
                pass
            if followers_posts_list:
                context = {'profile_list':profiles,'post_list':posts,'user_agent':user_agent,'create_form':create_form,
                'followers_posts_list':followers_posts_list,'following':following , 'followers':follower_count}
            else:
                context = {'profile_list':profiles,'post_list':posts,'user_agent':user_agent,'create_form':create_form}
            return render(request,'customers/index.html',context)
        else :
            return render(request,'members/login.html')


class PostDetail(OwnerDetailView):               
    model= Post
    template_name='customers/index.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['number_of_likes'] = likes_connected.number_of_likes()
        data['post_is_liked'] = liked
        return data


    

#standard way of creating the Post
class PostCreateView(LoginRequiredMixin, View):
    template_name = 'customers/create.html'
    success_url = reverse_lazy('customers:index')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving pic = form.save(commit=False)
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        
        return redirect(self.success_url)

def Likeview(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    ctx = {}
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        ctx = {'liked':False}
    else:
        post.likes.add(request.user)
        ctx = {'liked':True}
    return HttpResponseRedirect(reverse('customers:index'),ctx)

class DeletePost(OwnerDeleteView):
    model = Post
    template_name = 'customers/delete_post.html'
    success_message ='The Post was successfully deleted!'

def handler404(request,exception, *args, **argv):
    return render(request,'404.html', {})

def handler500(request, *args, **argv):
    return render(request,'404.html', {})


#creating the post using jquery and ajax and making it serialized
def post_create(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        print("success!")
        if request.method == "POST":
            post= request.POST["message"]
            new_post =Post.objects.create(text=post,owner=request.user)
            res= serializers.serialize('json',[new_post,])
            return JsonResponse({"instance": res}, status=200)
        else:
             return JsonResponse({"error": request.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)


def commentcreate(request , pk):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        print("success!")
        if request.method == "POST":
            post = get_object_or_404(Post,id=pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment= Comment(text=form.text,owner=request.user,post=post)
                comment.save()
                ser=serializers.serialize('json', [ comment, ])
                return JsonResponse({"instance": ser}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": ""}, status=400)



def Testview(request):
    if request.user.is_authenticated :
        posts=Post.objects.all().order_by('-created_at')
        profiles=Profile.objects.all()
        user_agent = get_user_agent(request).browser.family
        #passing the create form to the main page
        create_form = CreateForm()

        followers_posts_list = {}
        try:
            userobject = get_object_or_404(Profile, user=request.user)
            followers=Follwing_count.objects.filter(follwer=userobject.user)
            following = len(Follwing_count.objects.filter(follwing=userobject.user))
            follower_count = len(followers)
            for follower in followers :
                user_object = User.objects.get(username=follower)
                followers_posts_list=Post.objects.filter(owner=user_object)
        except:
            pass
        if followers_posts_list:
            context = {'profile_list':profiles,'post_list':posts,'user_agent':user_agent,'create_form':create_form,
                'followers_posts_list':followers_posts_list,'following':following , 'followers':follower_count}
        else:
            context = {'profile_list':profiles,'post_list':posts,'user_agent':user_agent,'create_form':create_form}
        return render(request,'navbar.html',context)
    else : 
        return render(request,'members/register.html')



    


        