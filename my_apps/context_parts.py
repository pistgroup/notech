from my_apps.models import Category, Service, Tags, ServiceFavorite
from accounts.models import Profile
from django.db.models import Avg, Min, Max
from .forms import *


def common(request):
    #テンプレートに毎回渡す値
    context = {
        'category_list' : Category.objects.all(),
        'tags_list': Tags.objects.all(),
        'service_list': Service.objects.all(),
        'profile_list': Profile.objects.all(),
        'price_order_min': Service.objects.order_by('amount'),
        'price_order_max': Service.objects.order_by('-amount'),
        'site_title':'農家マッチングNotech(ノーテック)',
    }
    return context

