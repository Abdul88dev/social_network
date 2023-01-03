from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'members'
urlpatterns = [
    path('/login', views.login_user, name='login'),
    path('/logout', views.logout_user, name='logout'),
    path('/register', views.register_user, name='register'),
    path('/follow', views.follwingview, name='follow'),
    path('/profile/<slug:slug>',views.UserProfiles.as_view(),name="users-profile"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)