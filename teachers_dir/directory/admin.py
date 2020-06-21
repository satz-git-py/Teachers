from django.contrib import admin
from .models import Teacher
from import_export.admin import ImportExportModelAdmin

# Register your models here.
#admin.site.register(Teacher)
@admin.register(Teacher)

#class TeacherAdmin(admin.ModelAdmin):
class TeacherAdmin(ImportExportModelAdmin):
    pass