from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('study_tools.urls')),  # replace 'myapp' with your app's name
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')), 
]
