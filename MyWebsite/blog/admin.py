from django.contrib import admin
from .models import Post
from import_export.admin import ImportExportModelAdmin

@admin.register(Post)
class ViewAdmin(ImportExportModelAdmin):
    pass

# Register your models here.
