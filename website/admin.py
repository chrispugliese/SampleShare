from .models import UserProfile
from django.contrib import admin

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('email', 'username', 'created_at')

admin.site.register(UserProfile, UserProfileAdmin)