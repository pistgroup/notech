# coding: UTF-8
from django.conf import settings
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
from django.db.models import F, Sum, Avg



# Create your models here.

class Category(models.Model):
    #出品カテゴリ
    category_name = models.CharField('商品カテゴリ', max_length=200)
    image = StdImageField('カテゴリー画像', upload_to='category/', blank=True, variations={
        'medium': {"width": 400, "height": 400, "crop": True},
        'cover': {"width": 1920, "height": 720, "crop": True},

    })
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.category_name

class Tags(models.Model):
    #出品タグ
    tags_name = models.CharField('商品タグ', max_length=200)
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.tags_name

class CategoryTags(models.Model):
    #出品タグ
    tags_name = models.CharField('商品タグ', max_length=200)
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.tags_name

RANK_CHOICE = (
        ('Sランク', 'S'),
        ('Aランク', 'A'),
        ('Bランク', 'B'),
        ('Cランク', 'C'),
)

UNIT_CHOICE = (
        ('kg', 'kg'),
        ('個', '個'),
)
DELIVERY_DATE_CHOICE = (
        ('即日', '即日出荷'),
        ('1〜2営業日', '1〜2営業日出荷'),
        ('3〜4営業日', '3〜4営業日出荷'),
        ('4〜6営業日', '4〜6営業日出荷'),
        ('7営業日以降', '7営業日以降出荷'),
)

class Service(models.Model):
    #出品者
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='出品ユーザー', on_delete=models.PROTECT)
    image01 = StdImageField('カバー画像1', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},

    })
    image02 = StdImageField('カバー画像2', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},
    })
    image03 = StdImageField('カバー画像3', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},
    })
    image04 = StdImageField('カバー画像4', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},
    })
    title = models.CharField('タイトル', max_length=30, blank=True)
    text = models.TextField('本文', max_length=1000, blank=True)
    category = models.ForeignKey(Category, verbose_name='商品カテゴリ', on_delete=models.PROTECT, blank=True)
    tags = models.ManyToManyField(Tags, related_name='tag', verbose_name="品種タグ", blank=True)
    categorytags = models.ManyToManyField(CategoryTags, related_name='categorytag', verbose_name="品種タグ", blank=True)
    delivery_date = models.CharField('出荷日', max_length=15, choices=DELIVERY_DATE_CHOICE, blank=True)
    rank = models.CharField('商品ランク', max_length=15, choices=RANK_CHOICE, blank=True)
    unit = models.CharField('単位', max_length=15, choices=UNIT_CHOICE, blank=True)
    amount = models.PositiveIntegerField(verbose_name='金額', default=0)
    date = models.DateTimeField('更新日', default=timezone.now)

    def favorite_count(self):
        return ServiceFavorite.objects.filter(post=self).count()

    def avg_rating(self):
        return ServiceComments.objects.filter(post=self, rating__gt=0).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0


    def __str__(self):
        return '{0}{1}{2}'.format(self.title, self.amount, self.user.email)



class ServiceComments(models.Model):
    #コメント機能
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.PROTECT)
    post = models.ForeignKey(Service, verbose_name='紐づく記事', on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name='評価', default=0)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField('一言')
    date = models.DateTimeField('更新日', default=timezone.now)

    def dates(self):
        return self.date.strftime('%Y/%m/%d %H:%M')

    def __str__(self):
        return self.text[:10]

class ServiceFavorite(models.Model):
    #コメント機能
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.CASCADE)
    post = models.ForeignKey(Service, verbose_name='紐づく記事', on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return '{} {}'.format(self.user.email, self.post.title)





class DM(models.Model):
    #DM機能
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.PROTECT, null=True)
    text = models.TextField('メッセージ本文')
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.text[:10]
