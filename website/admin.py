from django.contrib import admin
from website.models import Profile
from website.models import UserImages

# Register your models here.

class ProfileAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

admin.site.register(Profile, ProfileAdminView)



class UserImageAdminView(admin.ModelAdmin):
    list_display = [field.name for field in UserImages._meta.fields]

admin.site.register(UserImages, UserImageAdminView)
