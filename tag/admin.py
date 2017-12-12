from django import forms
from django.contrib import admin
from .models import User1, UserInfo, ClientInfo

# Register your models here.

admin.site.register(User1)


# class UserInfoForm(forms.ModelForm):
#     class Meta:
#         model = UserInfo
#         exclude = ['user_time']


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):

    def user_name(self, obj):
        return obj.user.email

    user_name.short_description = 'email'

    def time(self, obj):
        return obj.user_time.strftime('%I:%M:%S') + "  "+obj

    list_display = ('user_tag', 'user_name', 'time')


# admin.site.register(UserInfo, )
admin.site.register(ClientInfo)
