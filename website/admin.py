from django.contrib import admin
from .models import UserProfile, Chat, Message
from .models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
    ]


# Register your models here.
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Sample)

class MessageInline(admin.TabularInline):  # Use TabularInline for a table-like display, or StackedInline for a stacked display
    model = Message
    extra = 0  # Set to 0 to avoid showing extra blank message forms
    fields = ('user', 'content')  # Fields you want to display in the inline
    readonly_fields = ('created_at',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'chatTimeStamp')  # Customize the list display
    inlines = [MessageInline]  # Add the inline to the Chat admin