from django import forms
from .models import *

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


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class ServiceFavoriteCreate(forms.ModelForm):
    class Meta:
        model = ServiceFavorite
        fields = ('post',)

class ServiceCommentsCreate(forms.ModelForm):
    class Meta:
        model = ServiceComments
        fields = ('rating', 'text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['style'] = 'display:none'

class ServiceCommentsReply(forms.ModelForm):
    class Meta:
        model = ServiceComments
        fields = ('text',)


class DMCreate(forms.ModelForm):
    class Meta:
        model = DM
        fields = ('text','date')