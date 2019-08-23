from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='change-password'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('done/', views.UserCreateDone.as_view(), name='user_create_done'),
    path('complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('profile_create/', views.profilecreate, name='profile_create'),
    path('profile_detail/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile_update/<int:pk>/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('follow/<int:pk>/', views.followPlace, name='follow'),
]
