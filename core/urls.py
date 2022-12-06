from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('events/<str:pk>', views.events, name='events'),
    path('explore', views.explore, name='explore'),
    path('post/<str:pk>', views.post, name='post'),
    path('follow', views.follow, name='follow'),
    path('like/<str:pk>', views.like, name='like'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('logout', views.logout, name='logout'), 
    path('createpost/', views.createpost, name='createpost'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('deletepost/<str:pk>', views.deletepost, name='deletepost'),  
    path('editpost/<str:pk>', views.editpost, name='editpost'),
    path('forgetpassword', views.forgetpassword, name='forgetpassword'),  
]      