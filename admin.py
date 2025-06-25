from django.contrib import admin
from .models import BuildingProject

@admin.register(BuildingProject)
class BuildingProjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'standort', 'created')
    list_filter  = ('created',)
    search_fields = ('standort',)
    ordering     = ('-created',)