from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404,render_to_response
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, resolve_url
from django.template.loader import get_template
from django.views import generic
from .forms import LoginForm, UserCreateForm, ProfileCreateForm, ProfileUpdateForm
from .models import Profile, Follow
from my_apps.models import Service, CategoryTags
from cart.models import BuyingHistory
from django.contrib import messages


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'registration/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'registration/logout.html'

class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'registration/create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject_template = get_template('registration/mail_template/subject.txt')
        subject = subject_template.render(context)

        message_template = get_template('registration/mail_template/message.txt')
        message = message_template.render(context)

        user.email_user(subject, message)
        return redirect('accounts:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'registration/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'registration/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)

            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


def ProfileCreate(request):
    form = ProfileCreateForm(request.POST or None)
    if form.is_valid():
        test = form.save(commit=False)
        test.user_id = request.user.id
        test.save()
        return redirect('my_apps:mypage')
    context = {
        'form': form
    }
    return render(request, 'my_apps/form.html', context)

class ProfileListView(generic.ListView):
    model = Profile
    template_name = 'my_apps/categories.html'
    paginate_by = 1

   # def get_queryset(self):
    #    return Service.objects.filter(user=self.request.user)

class ProfileDetail(generic.DetailView):
    model = Profile
    template_name = 'my_apps/channel-mypage.html'


class ProfileUpdate(OnlyYouMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'my_apps/form.html'
    success_url = reverse_lazy('my_apps:index')

class UserSystem(generic.TemplateView):
    model = BuyingHistory
    template_name = 'my_apps/user-system.html'


class UserSystemService(generic.TemplateView):
    model = Profile
    template_name = 'my_apps/user-system-service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buyinghistory_list']= BuyingHistory.objects.all()
        context['profile_l'] = Profile.objects.filter(user=self.request.user)
        print(context)
        return context

class UserSystemBuy(generic.ListView):
    model = BuyingHistory
    template_name = 'my_apps/user-system-buy.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

class Followadd(generic.CreateView):
    model = Follow


class FollowList(generic.ListView):
    model = Follow
    template_name = 'my_apps/categories.html'