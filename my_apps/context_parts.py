from .models import Category
from accounts.models import Profile


def common(request):
    context = {
        'category_list' : Category.objects.all()
    }
    return context

