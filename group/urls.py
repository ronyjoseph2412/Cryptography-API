from django.urls import path
from . import views
from knox import views as knox_views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('getuser', views.get_user),
    path('creategroup', views.create_group),
    path('getlog', views.create_group),
    path('getgroups', views.get_group_activity),
    path('generateshares', views.post_data_for_sss),
    path('commitshare', views.commit_share),
    path('getshare', views.get_secret),
]