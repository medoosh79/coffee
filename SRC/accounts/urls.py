from django import urls
from django.conf.urls import include
from django.urls import path
from . import views


urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('product_favorite/<int:pro_id>', views.product_favorite, name='favorite'),
    path('show_favorite', views.show_favorite, name='show_favorite'),
    path('profile_edite', views.profile_edite, name='profile_edite'),
    path('logout', include('django.contrib.auth.urls')),
    
    
]
