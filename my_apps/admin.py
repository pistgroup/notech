from django.contrib import admin
from .models import Category, Tags, Service, Order, ServiceComments, DM

admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(ServiceComments)
admin.site.register(DM)

