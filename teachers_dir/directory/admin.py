#from tablib import dataset
from django.contrib import admin
from .models import Teacher
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
#admin.site.register(Teacher)
@admin.register(Teacher)

#class TeacherAdmin(admin.ModelAdmin):
class TeacherAdmin(ImportExportModelAdmin):
    pass

class TeacherResource(resources.ModelResource):
    class meta:
        model = Teacher
    
    def before_import(self, dataset, dry_run):
        # Make standard corrections to the dataset
        # Convert headers to lower case
        if dataset.headers:
            dataset.headers = [str(header).lower().strip() for header in dataset.headers]

    def skip_row(self, instance, original):
        
        return super(YourResource, self).skip_row(instance, original)