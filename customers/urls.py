from django.urls import path ,reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'customers'
urlpatterns = [
    path('', views.Mainview.as_view(), name='index'),
    path('/post/create',
        views.PostCreateView.as_view(success_url=reverse_lazy('customers:index')), name='post_create'),
    path('like/<int:pk>',views.Likeview, name="like_post"),
    path('/post/delete/<int:pk>',
        views.DeletePost.as_view(success_url=reverse_lazy('customers:index')), name='post_delete'),
    path('post/ajax/create',views.post_create , name='post_create_ajax'),
    path('test',views.Testview , name='test-view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)