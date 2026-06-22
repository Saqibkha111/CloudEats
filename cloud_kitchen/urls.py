
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.http import HttpResponse
from kitchen import views






def profile_view(request):
    return HttpResponse("<h2>Welcome to your profile page!</h2>")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kitchen.urls')),    
    path('', views.index, name='index'),        
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', include('kitchen.urls_register')),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/login/', views.login_view, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
