from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    ,blank=True)
    text = models.TextField(blank=True,null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')
    main_img = models.ImageField(upload_to='images/',null=True, blank=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,related_name="post_likes",blank=True)
    #shows The likes numbers
    def number_of_likes(self):
        return self.likes.count()

    def comments_list(self):
        return self.comments.all()
    
    #returns the publish date
    def publish_date(self):
        return self.updated_at.strftime("%b-%Y")
    # Shows up in the admin list
    def __str__(self):
        return self.text


class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11]


class StoryModel(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_user')
        content = models.ImageField(upload_to='images/')
        caption = models.TextField(max_length=50)
        expired = models.BooleanField(default=False)
        posted = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.user.username
