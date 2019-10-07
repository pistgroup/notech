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
    path('profile_create/', views.ProfileCreate, name='profile_create'),
    path('profile_list/', views.ProfileListView.as_view(), name='profile_list'),
    path('profile_detail/<int:pk>/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile_update/<int:pk>/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('user_system/', views.UserSystem.as_view(), name='user_system'),
    path('user_system/service/', views.UserSystemService.as_view(), name='user_system_service'),
    path('user_system/buy', views.UserSystemBuy.as_view(), name='user_system_buy'),
    path('follow/', views.FollowList.as_view(), name='follow'),
]
