from django.contrib import admin
from .models import Teacher
from import_export.admin import ImportExportModelAdmin
from import_export import resources
#from directory.filters import FirstLetterFilter
from django.contrib.admin import SimpleListFilter
from import_export.results import RowResult
import json

# json import for custom configurations and exception handlings
'''
with open('directory_config.json') as f:
    directory_config = json.load(f)
'''

# these configuration details will fo into json file or into the model
json_config = """
{
    "subject_taught": {
        "limit": 5,
        "err_msg": "Teachers are allowed to teach only 5 subjects"
    },
    "first_name": {
        "empty": {
            "err_msg": "First name should not be emplty or null value"
        }
    },
    "last_name": {
        "empty": {
            "err_msg": "First name should not be emplty or null value"
        }
    }    
}
"""
# deserialization json data of string to json object
directory_config = json.loads(json_config)

# class to add filter by first letter of "Last_Name"
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

# increased the scope of the import_result 
# so that it can be used for the custom errors in ModelResource class 
global import_result

# modelresource to skip the records with import errors and custom exceptions
class ModelResource(resources.ModelResource):

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Copy the values to display in the preview report
            import_result.diff = [row[val] for val in row]
            #print(import_result.diff[6])

            # Add a column with the error message
            import_result.diff.append('Errors: {}'.format([err.error for err in import_result.errors]))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP
        else:
            if len(row['Subjects_Taught'].split(',')) > directory_config['subject_taught']['limit']:
                import_result.diff = [row[val] for val in row]
                import_result.diff.append('Custom Exception: {}'.format(directory_config['subject_taught']['err_msg']))
                import_result.errors = []
                import_result.import_type = RowResult.IMPORT_TYPE_SKIP
            elif row['First_Name'] == '' or row['First_Name'] == ' ':
                import_result.diff = [row[val] for val in row]
                import_result.diff.append('Custom Exception: {}'.format(directory_config['first_name']['empty']['err_msg']))
                import_result.errors = []
                import_result.import_type = RowResult.IMPORT_TYPE_SKIP
            elif row['Last_Name'] == '' or row['Last_Name'] == ' ':
                import_result.diff = [row[val] for val in row]
                import_result.diff.append('Custom Exception: {}'.format(directory_config['last_name']['empty']['err_msg']))
                import_result.errors = []
                import_result.import_type = RowResult.IMPORT_TYPE_SKIP
                           
        return import_result

    class Meta:
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        model = Teacher

# Resource class handle the import of data
class TeacherResource(resources.ModelResource):
    class meta:
        model = Teacher
        import_id_fields = ('Email_Address',)
        fields = ('Email_Address', 'First_Name', 'Last_Name', 'Profile_Picture', 'Phone_Number', 'Room_Number', 'Subjects_Taught')
    
    # def before_import(self, dataset, dry_run):
    #     # Make standard corrections to the dataset
    #     # Convert headers to lower case
    #     if dataset.headers:
    #         dataset.headers = [str(header).lower().strip() for header in dataset.headers]
    #         print('*******************',dataset.headers,'*******************')

    def skip_row(self, instance, original):
        #logic to skip the record
        print('*******************',instance,'*******************')
        print('*******************',original,'*******************')
        return super(TeacherResource, self).skip_row(instance, original)


class TeacherAdmin(ImportExportModelAdmin):
    
    resource_class = ModelResource

    list_fields = ('First_Name', 'Last_Name', 'Profile_Picture', 'Email_Address', 'Phone_Number', 'Room_Number', 'Subjects_Taught')
    search_fields = ('First_Name', 'Last_Name', 'Email_Address', 'Subjects_Taught')
    #readonly_fields = ('First_Name', 'Last_Name', 'Email_Address')

    filter_horizontal = ()
    list_filter = [ FirstLetterFilter,]

admin.site.register(Teacher, TeacherAdmin)
