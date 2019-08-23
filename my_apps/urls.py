from django.urls import path
from . import views

app_name = 'my_apps'

urlpatterns = [

	path('', views.LPView.as_view(), name='index'),#myapps/の後に何も付かない場合
	path('mypage/', views.mypage, name='mypage'),
	path('service/', views.servicecreate, name='service'),
	path('service_list/', views.ServiceListView.as_view(), name='service_list'),
	path('search/', views.ServiceSearchView.as_view(), name='service_search_list'),
	path('service_detail/<int:pk>', views.ServiceDetailView.as_view(), name='service_detail'),
	path('service_update/<int:pk>', views.ServiceUpdateView.as_view(), name='service_update'),
	path('comments/<int:post_pk>', views.ServiceCommentsView.as_view(), name='comments'),
	path('dm_list/', views.DmList.as_view(), name='dm_list'),

]
