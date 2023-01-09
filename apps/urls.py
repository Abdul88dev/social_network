from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('members',include('members.urls')),
    path('', include('customers.urls')),
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
]

handler404="customers.views.handler404"
handler500="customers.views.handler500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


