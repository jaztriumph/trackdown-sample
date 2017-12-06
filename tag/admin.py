from django.contrib import admin
from .models import User1,UserManager,UserInfo,ClientInfo

# Register your models here.

admin.site.register(User1)
# admin.site.register(UserManager)
admin.site.register(UserInfo)
admin.site.register(ClientInfo)