from django.contrib import admin
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
	list_display = ['from_email', 'sent_at', 'subject']
	list_filter = ['sent_at']
	search_fields = ['from_email']

admin.site.register(Contact, ContactAdmin)
