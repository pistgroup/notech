# coding: UTF-8
from django.conf import settings
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField
# Create your models here.

class Category(models.Model):
    #出品カテゴリ
    category_name = models.CharField('商品カテゴリ', max_length=200)
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.category_name

class Tags(models.Model):
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    image01 = StdImageField('サムネイル', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},

    })
    image02 = StdImageField('サムネイル', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},
    })
    image03 = StdImageField('サムネイル', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},
    })
    image04 = StdImageField('サムネイル', upload_to='service/', blank=True, variations={
        'large': {"width": 1280, "height": 720, "crop": True},
        'medium': {"width": 720, "height": 400, "crop": True},
    })
    title = models.CharField('タイトル', max_length=200, blank=True)
    text = models.TextField('本文', blank=True)
    category = models.ForeignKey(Category, verbose_name='商品カテゴリ', on_delete=models.PROTECT, blank=True)
    delivery_date = models.CharField('出荷日', max_length=15, choices=DELIVERY_DATE_CHOICE, blank=True)
    tags = models.ManyToManyField(Tags, verbose_name="商品タグ", blank=True)
    rank = models.CharField('商品ランク', max_length=15, choices=RANK_CHOICE, blank=True)
    unit = models.CharField('単位', max_length=15, choices=UNIT_CHOICE, blank=True)
    amount = models.PositiveIntegerField(verbose_name='金額', default=0)
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return '{0}{1}{2}'.format(self.user.email, self.category, self.title)


class Order(models.Model):
    #購入者
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=200, blank=True)
    text = models.TextField('本文', blank=True)
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.title

class ServiceComments(models.Model):
    #コメント機能
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.PROTECT, null=True)
    post = models.ForeignKey(Service, verbose_name='紐づく記事', on_delete=models.PROTECT)
    text = models.TextField('一言')
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.text[:10]

class DM(models.Model):
    #DM機能
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='ユーザー', on_delete=models.PROTECT, null=True)
    text = models.TextField('メッセージ本文')
    date = models.DateTimeField('更新日', default=timezone.now)

    def __str__(self):
        return self.text[:10]
