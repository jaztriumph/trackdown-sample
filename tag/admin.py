from django import forms
from django.contrib import admin
from .models import User1, UserInfo, ClientInfo
from django.utils.html import format_html


# Register your models here.

@admin.register(User1)
class User1Admin(admin.ModelAdmin):
    def full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    list_display = ('email', 'full_name')
    search_fields = ['^email', '^first_name', '^last_name']
    list_filter = (
        ('is_staff', admin.BooleanFieldListFilter),
    )


# class UserInfoForm(forms.ModelForm):
#     class Meta:
#         model = UserInfo
#         exclude = ['user_time']

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'email'

    def time(self, obj):
        return obj.user_time.strftime('%I:%M:%S - %d %b %y')

    time.admin_order_field = "user_time"

    list_display = ('user_tag', 'user_email', 'time',)
    # list_display_links = ('user_email',)
    # list_editable = ('user_tag',)
    # list_per_page=2
    # list_select_related = ()

    # used for user selection
    # radio_fields = {"user": admin.VERTICAL}
    # raw_id_fields = ("user",)
    # save_on_top = True
    search_fields = ['^user__email', '^user_tag']


# admin.site.register(UserInfo, )
@admin.register(ClientInfo)
class ClientInfoAdmin(admin.ModelAdmin):
    def user_email(self, obj):
        return obj.user_info.user.email

    user_email.short_description = 'email'

    def user_tag(self, obj):
        return obj.user_info.user_tag

    user_tag.short_description = 'tag'

    def time(self, obj):
        return obj.client_time.strftime('%I:%M:%S - %d %b %y')

    time.admin_order_field = "client_time"

    list_display = ['user_tag', 'user_email', 'time', 'client_agent']
    search_fields = ['^user_info__user__email', '^user_info__user_tag']
