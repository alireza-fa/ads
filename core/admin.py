from django.contrib import admin

from .models import UserCompanyExtend, UserInfluExtend, Contact


admin.site.register(UserCompanyExtend)

admin.site.register(UserInfluExtend)

admin.site.register(Contact)
