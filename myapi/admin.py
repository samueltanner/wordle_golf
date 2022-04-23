from django.contrib import admin
from .models import Score, GolfGroup, User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Score)
admin.site.register(GolfGroup)
admin.site.register(User, UserAdmin)
