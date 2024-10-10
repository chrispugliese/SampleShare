from django.contrib import admin
from .models import UserProfile, Sample


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
    ]


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Sample)
