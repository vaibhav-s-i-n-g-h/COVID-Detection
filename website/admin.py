from django.contrib import admin
from website.models import Profile

# Register your models here.

class ProfileAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

admin.site.register(Profile, ProfileAdminView)