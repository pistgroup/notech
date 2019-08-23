# coding: UTF-8
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from stdimage.models import StdImageField  #追記
from my_apps.models import Service

class UserManager(BaseUserManager):
    """ユーザーマネージャー."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールアドレスでの登録を必須にする"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """is_staff(管理サイトにログインできるか)と、is_superuer(全ての権限)をFalseに"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """スーパーユーザーは、is_staffとis_superuserをTrueに"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル."""

    email = models.EmailField(_('メールアドレス'), unique=True)
    first_name = models.CharField(_('性'), max_length=30, blank=True)
    last_name = models.CharField(_('名'), max_length=30, blank=True)


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        """username属性のゲッター

        他アプリケーションが、username属性にアクセスした場合に備えて定義
        メールアドレスを返す
        """
        return self.email

FROM_CHOICE = (
    ('北海道', '北海道'),
    ('青森県', '青森県'),
    ('岩手県', '岩手県'),
    ('宮城県', '宮城県'),
    ('秋田県', '秋田県'),
    ('山形県', '山形県'),
    ('福島県', '福島県'),
    ('茨城県', '茨城県'),
    ('栃木県', '栃木県'),
    ('群馬県', '群馬県'),
    ('埼玉県', '埼玉県'),
    ('千葉県', '千葉県'),
    ('東京都', '東京都'),
    ('神奈川県', '神奈川県'),
    ('新潟県', '新潟県'),
    ('富山県', '富山県'),
    ('石川県', '石川県'),
    ('広島県', '広島県'),
    ('山口県', '山口県'),
    ('長野県', '長野県'),
    ('岐阜県', '岐阜県'),
    ('静岡県', '静岡県'),
    ('愛知県', '愛知県'),
    ('三重県', '三重県'),
    ('滋賀県', '滋賀県'),
    ('京都府', '京都府'),
    ('大阪府', '大阪府'),
    ('兵庫県', '兵庫県'),
    ('奈良県', '奈良県'),
    ('和歌山県', '和歌山県'),
    ('鳥取県', '鳥取県'),
    ('島根県', '島根県'),
    ('岡山県', '岡山県'),
    ('福井県', '福井県'),
    ('山梨県', '山梨県'),
    ('徳島県', '徳島県'),
    ('香川県', '香川県'),
    ('愛媛県', '愛媛県'),
    ('高知県', '高知県'),
    ('福岡県', '福岡県'),
    ('佐賀県', '佐賀県'),
    ('長崎県', '長崎県'),
    ('熊本県', '熊本県'),
    ('大分県', '大分県'),
    ('宮崎県', '宮崎県'),
    ('鹿児島県', '鹿児島県'),
    ('沖縄県', '沖縄県'),

)

class UserInfomation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    image01 = StdImageField('カバー画像1枚目', upload_to='img/', blank=True, variations={
        'medium': {"width": 400, "height": 400, "crop": True},
        'cover': {"width": 1920, "height": 720, "crop": True},
    })
    text01 = models.TextField('テキスト1枚目', blank=True)
    image02 = StdImageField('カバー画像2枚目', upload_to='img/', blank=True, variations={
        'medium': {"width": 400, "height": 400, "crop": True},
        'cover': {"width": 1920, "height": 720, "crop": True},
    })
    text02 = models.TextField('テキスト2枚目', blank=True)
    service = models.ForeignKey(Service, verbose_name='投稿サービス', on_delete=models.PROTECT),

"""場所の情報"""
class Follow(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_follow = models.BooleanField(_('フォロー'), default=False,)

    def __str__(self):
        return self.user.email


class Profile(models.Model):
    '''個人情報'''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user_name = models.CharField('氏名', max_length=15, blank=True)
    user_nickname = models.CharField('ユーザーネーム', max_length=15, blank=True)
    image_profile = StdImageField('プロフィール画像', upload_to='img/', blank=True, variations={
        'thumbnail': {"width": 150, "height": 150, "crop": True},
        'medium': {"width": 400, "height": 400, "crop": True},
    })
    image_cover = StdImageField('カバー画像', upload_to='img/', blank=True, variations={
        'cover': {"width": 1920, "height": 720, "crop": True},
    })
    user_from = models.CharField('居住エリア', max_length=15, choices=FROM_CHOICE)
    user_address = models.CharField('配達先', max_length=300, blank=True)
    user_text = models.TextField('自己紹介(160文字以内)', blank=True, max_length=160)
    user_follow = models.ManyToManyField(Follow, verbose_name='フォロー', blank=True, null=True)
    user_cleate_date = models.DateTimeField('作成日', default=timezone.now)
    user_update_date = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return '{0}{1}'.format(self.user_address, self.user_update_date)

