from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Message

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + ((None, {"friends": ("friends",)}),)
    filter_horizontal = ('friends', )

admin.site.register(CustomUser)
admin.site.register(Message)
