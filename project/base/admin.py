from django.contrib import admin
from .models import Contact,User, Profile,SiteAnnouncement,Message,ContactSupport

# Register your models here.
class ContactRef(admin.ModelAdmin):
    list_display = ['name','email','phone']

admin.site.register(Contact,ContactRef)
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(SiteAnnouncement)
admin.site.register(Message)
admin.site.register(ContactSupport)