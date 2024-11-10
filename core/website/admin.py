from django.contrib import admin
from .models import ContactModel, NewsLetter

@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'subject', 'is_seen', 'created_date')
    list_filter = ('is_seen', 'created_date')
    search_fields = ('full_name', 'email', 'phone_number', 'subject', 'content')

@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    search_fields = ('email',)
