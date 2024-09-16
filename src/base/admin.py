from django.contrib import admin

from base.models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    pass