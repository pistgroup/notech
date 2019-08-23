from django import forms
from .models import Service, Order, ServiceComments, DM

class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('title', 'image01','image02','image03','image04','text', 'tags', 'category', 'rank', 'amount', 'unit')
        widgets = {
            'title':forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'わからないこと、解決したいことを10文字以上で書いてください',
        })
        }

class OrderCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ServiceUpdateForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = '__all__'


class ServiceCommentsCreate(forms.ModelForm):
    class Meta:
        model = ServiceComments
        fields = ('text', 'date')

class DMCreate(forms.ModelForm):
    class Meta:
        model = DM
        fields = ('text','date')