from django.contrib import admin
from .models import DataSet, DataSetValue


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    pass


@admin.register(DataSetValue)
class DaaSetValueAdmin(admin.ModelAdmin):
    pass
