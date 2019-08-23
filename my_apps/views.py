from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404, render_to_response
from django.db.models import Q, Count #検索でorが使えるモジュール
from django.urls import reverse_lazy
from .models import Service, ServiceComments, DM
from accounts.models import Profile
from .forms import ServiceCreateForm, ServiceUpdateForm, ServiceCommentsCreate, DMCreate
from django.views import generic

class LPView(generic.ListView):
    model = Service
    template_name = 'my_apps/index.html'
    #count = Service.objects.count()

def mypage(request):

    context={
        'profile_list':Profile.objects.all(),
        'service_list':Service.objects.all(),
    }

    return render(request, 'my_apps/mypage.html', context)


class ServiceSearchView(generic.ListView):
    model = Service
    template_name = 'my_apps/search.html'


    def get_queryset(self):
        query_set = Service.objects.all()
        keyword = self.request.GET.get('keyword')
        if keyword:
            query_set = query_set.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )#__icontainsをつけるとタイトルを含むかどうか Qでorが使える
            return query_set


def servicecreate(request):
    form = ServiceCreateForm(request.POST or None, request.FILES)
    if form.is_valid():
        test = form.save(commit=False)
        test.user_id = request.user.id
        test.save()
        return redirect('my_apps:mypage')
    context = {
        'form': form
    }
    return render(request, 'my_apps/form.html', context)


class ServiceListView(generic.ListView):
    model = Service
    template_name = 'my_apps/service-list.html'
    paginate_by = 1

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'my_apps/service-detail.html'



class ServiceUpdateView(generic.UpdateView):
    model = Service
    form_class = ServiceUpdateForm
    template_name = 'my_apps/form.html'
    success_url = reverse_lazy('my_apps:index')

    def form_valid(self, form):
        self.object = service = form.save()
        messages.info(self.request, f'記事を作成しました。 タイトル:{service.title} pk:{service.pk}')
        return redirect(self.get_success_url())

class ServiceCommentsView(generic.CreateView):
    model = ServiceComments
    form_class = ServiceCommentsCreate
    template_name = 'my_apps/service-comments.html'

    def form_valid(self, form):
        post_pk = self.kwargs['post_pk']
        comment = form.save(commit=False) #この段階ではDBにコメントは保存されていない
        comment.user = self.request.user #ログインユーザーを取得
        comment.post = get_object_or_404(Service, pk=post_pk)
        comment.save()
        return redirect('my_apps:service_detail', pk=post_pk)

class DmList(generic.ListView):
    model = DM
    template_name = 'my_apps/dm.html'