from django.contrib import admin

from .models import UserCompanyExtend, UserInfluExtend, Contact, Basket, ContactUs


admin.site.register(UserCompanyExtend)

admin.site.register(UserInfluExtend)

admin.site.register(Contact)

admin.site.register(Basket)

admin.site.register(ContactUs)
