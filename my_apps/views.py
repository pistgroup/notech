from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404, render_to_response
from django.db.models import Q, Count, Max #検索でorが使えるモジュール
from django.urls import reverse_lazy
from accounts.models import Profile
from cart.models import *
from django.db.models import F, Sum, Avg
from .forms import *
from django.views import generic
from django.contrib.auth.decorators import login_required

class LPView(generic.ListView):
    model = Service
    template_name = 'my_apps/index.html'


    def get_queryset(self):
        context = {
            'maxamount': Service.objects.filter(amount__gte=100).count(),
            'maxamount2': Service.objects.aggregate(Max('amount')),
        }
        try:
            int = context['maxamount2']
            key = int['amount__max']
            price = context['maxamount'] * key
            print(price)
            return context
        except:
            return context

    def get_context_data(self, **kwargs):
        context = super(LPView, self).get_context_data(**kwargs)

        print(context)
        return context



@login_required
def Mypage(request):

    context={
        'profile_list':Profile.objects.all(),
        'service_list':Service.objects.all(),
    }
    return render(request, 'my_apps/channel-mypage.html', context)


class ServiceSearchView(generic.ListView):
    model = Service
    template_name = 'my_apps/category-seach.html'

    def get_queryset(self):
        query_set = Service.objects.all()
        keyword = self.request.GET.get('keyword')
        if keyword:
            query_set = query_set.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )#__icontainsをつけるとタイトルを含むかどうか Qでorが使える
            return query_set


def ServiceCreate(request):
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
    template_name = 'my_apps/channels.html'
    paginate_by = 1

   # def get_queryset(self):
    #    return Service.objects.filter(user=self.request.user)



class ServiceDetailView(generic.DetailView):
    model = Service
    form_class = ServiceCommentsCreate
    template_name = 'my_apps/single-video-tabs.html'

    def get_context_data(self, **kwargs):
        pk=self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context.update({
            'servicefavorite_list': ServiceFavorite.objects.all(),
            'favorite': ServiceFavoriteCreate(),
            'comments': ServiceCommentsCreate(),
            'comment_list': self.object.servicecomments_set.filter(parent__isnull=True),
            'comment_count': self.object.servicecomments_set.filter(rating__gt=0).count(),
            'favorite_active': '_border',
            'servicefavorite_filter': ServiceFavorite.objects.filter(user=self.request.user, post=pk),
        })
        if context['servicefavorite_filter']:
            context['favorite_active'] = ''



        return context



class ServiceConfirmView(generic.FormView):
    model = Service
    form_class = ServiceCommentsCreate
    template_name = 'registration/service-confirm.html'


    def form_valid(self, form):
        return render(self.request, 'my_apps/service-confirm.html', {'form': form})

    def form_invalid(self, form):
        return render(self.request, 'my_apps/service-confirm.html', {'form': form})


class ServiceUpdateView(generic.UpdateView):
    model = Service
    form_class = ServiceUpdateForm
    template_name = 'my_apps/form.html'
    success_url = reverse_lazy('my_apps:index')

    def form_valid(self, form):
        self.object = service = form.save()
        messages.info(self.request, f'記事を作成しました。 タイトル:{service.title} pk:{service.pk}')
        return redirect(self.get_success_url())

def favorite_create(request, post_pk):
    service = get_object_or_404(Service, pk=post_pk)
    if request.method == 'POST':
        suser = ServiceFavorite.objects.filter(user=request.user, post=service).count()

        if suser == 0:
            s = ServiceFavorite.objects.create(user=request.user, post=service, active=True)
            s.save()

            messages.success(request, 'お気に入りに登録しました')
        else:
            z = ServiceFavorite.objects.filter(user=request.user, post=service)
            z.delete()
            messages.error(request, 'お気に入りから削除しました')


    return redirect("my_apps:service_detail", post_pk)


def comment_create(request, post_pk):

    """記事へのコメント作成"""
    service = get_object_or_404(Service, pk=post_pk)
    form = ServiceCommentsCreate(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = service
        comment.user = request.user
        comment.save()
        return redirect('my_apps:service_detail', pk=service.pk)

    context = {
        'form': form,
        'post': service
    }

    return redirect("my_apps:service_detail", post_pk, context)

def reply_create(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(ServiceComments, pk=comment_pk)
    post = comment.post
    form = ServiceCommentsReply(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.user = request.user
        reply.parent = comment
        reply.post = post
        reply.save()
        return redirect('my_apps:service_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    print(context)
    return render(request, 'my_apps/form.html', context)

class DmList(generic.ListView):
    model = DM
    template_name = 'my_apps/dm.html'