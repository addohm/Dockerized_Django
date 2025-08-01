from django.contrib import admin
from django.utils.timezone import now

from .models import Contact, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    readonly_fields = ('user',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'when_sent', 'replied', 'when_replied')
    readonly_fields = ('when_sent', 'when_replied')

    def save_model(self, request, obj, form, change):
        if 'replied' in form.changed_data:  # Check if 'replied' field was changed
            if obj.replied:
                obj.when_replied = now()  # Set when_replied to current datetime
            else:
                obj.when_replied = None  # Clear the when_replied field if unchecked
        super().save_model(request, obj, form, change)
