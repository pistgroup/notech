from django.urls import path
from . import views

app_name = 'my_apps'

urlpatterns = [

	path('', views.LPView.as_view(), name='index'),#myapps/の後に何も付かない場合
	path('mypage/', views.Mypage, name='mypage'),
	path('service/', views.ServiceCreate, name='service'),
	path('service_list/', views.ServiceListView.as_view(), name='service_list'),
	path('search/', views.ServiceSearchView.as_view(), name='service_search_list'),
	path('service_detail/<int:pk>', views.ServiceDetailView.as_view(), name='service_detail'),
	path('service_update/<int:pk>', views.ServiceUpdateView.as_view(), name='service_update'),
	path('service_confirm/<int:pk>', views.ServiceConfirmView.as_view(), name='service_confirm'),
	path('favorite/<int:post_pk>', views.favorite_create, name='favorite'),
	path('comments/<int:post_pk>', views.comment_create, name='comments'),
	path('reply/<int:comment_pk>/', views.reply_create, name='reply_create'),
	path('dm_list/', views.DmList.as_view(), name='dm_list'),

]
