from django.contrib import admin
from .models import *
from reversion.admin import VersionAdmin

class ReverseAdmin(VersionAdmin):    #変更
    class Meta:
        fields = '__all__'

admin.site.register(Category, ReverseAdmin)
admin.site.register(CategoryTags, ReverseAdmin)
admin.site.register(Tags, ReverseAdmin)
admin.site.register(Service, ReverseAdmin)
admin.site.register(ServiceFavorite, ReverseAdmin)
admin.site.register(ServiceComments, ReverseAdmin)
admin.site.register(DM, ReverseAdmin)

