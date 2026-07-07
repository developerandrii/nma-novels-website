from django.contrib import admin
from catalog.models import Novel, Genre, Tag, Creator, Chapter

class NovleAdmin(admin.ModelAdmin):
    list_display = ["title", "format", "status"]
    list_filter = ["status", "format"]
    search_fields = ["title",]
    

class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CreatorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ChapterAdmin(admin.ModelAdmin):
    search_fields = ['novel__title']


admin.site.register(Novel, NovleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Chapter, ChapterAdmin)
