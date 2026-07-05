from django.contrib import admin
from catalog.models import Novel


class NovleAdmin(admin.ModelAdmin):
    list_display = ["title", "format", "status"]
    list_filter = ["status", "format"]
    search_fields = ["title",]
    

admin.site.register(Novel, NovleAdmin)
