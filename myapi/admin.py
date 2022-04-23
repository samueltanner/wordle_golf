from django.contrib import admin
from .models import Score, GolfGroup, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Score)
admin.site.register(GolfGroup)

fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'phone_number')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, UserAdmin)
