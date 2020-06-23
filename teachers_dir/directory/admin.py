#from tablib import dataset
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher
from import_export.admin import ImportExportModelAdmin
from import_export import resources
#from directory.filters import FirstLetterFilter
from django.contrib.admin import SimpleListFilter

class FirstLetterFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'First Letter of Last Name'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'letter'
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        lookups = []
        for letter in self.letters:
            count = qs.filter(Last_Name__istartswith=letter).count()
            if count:
                lookups.append((letter, '{} ({})'.format(letter, count)))
        return lookups

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        filter_val = self.value()
        if filter_val in self.letters:
            return queryset.filter(Last_Name__istartswith=self.value())



# Register your models here.
#admin.site.register(Teacher)
@admin.register(Teacher)
#class TeacherAdmin(admin.ModelAdmin):

class TeacherAdmin(ImportExportModelAdmin):
    
    #resource_class = TeacherResource

    list_fields = ('First_Name', 'Last_Name', 'Profile_Picture', 'Email_Address', 'Phone_Number', 'Room_Number', 'Subjects_Taught')
    search_fields = ('First_Name', 'Last_Name', 'Email_Address', 'Subjects_Taught')
    #readonly_fields = ('First_Name', 'Last_Name', 'Email_Address')

    filter_horizontal = ()
    list_filter = [ FirstLetterFilter,]

class TeacherResource(resources.ModelResource):
    class meta:
        model = Teacher
        import_id_fields = ('Email_Address',)
        fields = ('Email_Address', 'First_Name', 'Last_Name', 'Profile_Picture', 'Phone_Number', 'Room_Number', 'Subjects_Taught')
    
    def before_import(self, dataset, dry_run):
        # Make standard corrections to the dataset
        # Convert headers to lower case
        if dataset.headers:
            dataset.headers = [str(header).lower().strip() for header in dataset.headers]

    def skip_row(self, instance, original):
        #logic to skip the record

        return super(TeacherResource, self).skip_row(instance, original)


'''
class ModelResource(resources.ModelResource):
    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(
            row, instance_loader, **kwargs
        )

        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]

            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result
'''