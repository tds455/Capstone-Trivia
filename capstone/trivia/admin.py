from django.contrib import admin
from .models import User, Userstats, IDcache

# Register your models here.
admin.site.register(User)
admin.site.register(Userstats)
admin.site.register(IDcache)