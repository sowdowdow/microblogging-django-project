from django.contrib import admin
from Microlly.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date", "update_date", "author")
    date_hierarchy = "creation_date"
    search_fields = ("title",)


# Register your models here.
admin.site.register(Post, PostAdmin)
