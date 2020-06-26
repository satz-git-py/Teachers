from django.contrib import admin
from .models import Teacher
from import_export.admin import ImportExportModelAdmin
from import_export import resources
# from directory.filters import FirstLetterFilter
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
    "Email_Address": {
        "empty": {
            "err_msg": "Email address should not be empty."
        }
    },
    "subject_taught": {
        "limit": 5,
        "max_limit": {
            "err_msg": "Teachers are allowed to teach only 5 subjects."
        }
    },
    "first_name": {
        "empty": {
            "err_msg": "First name should not be empty."
        }
    },
    "last_name": {
        "empty": {
            "err_msg": "Last name should not be empty."
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


# ModelResource sub-class of Resource class to skip the records with import errors and custom exceptions
class ModelResource(resources.ModelResource):

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(row, instance_loader, **kwargs)
        # Copy the values to display in the preview report
        import_result.diff = [row[val] for val in row]
        # condition to check the import errors
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            # Add a column with the error message
            import_result.diff.append('Errors: {}'.format([err.error for err in import_result.errors]))
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP
        else:
            if row['Email_Address'] == '' or row['Email_Address'] == ' ':
                # Adding a column for error with custom error message - 'empty' from json for email
                import_result.diff.append('Errors: {}'.format(directory_config['Email_Address']['empty']['err_msg']))
            elif len(row['Subjects_Taught'].split(',')) > directory_config['subject_taught']['limit']:
                # Adding a column for custom error message 'max_limit' from json
                import_result.diff.append('Errors: {}'.format(directory_config['subject_taught']['max_limit']['err_msg']))
            elif row['First_Name'] == '' or row['First_Name'] == ' ':
                # Adding a column for error with custom error message 'empty' from json
                import_result.diff.append('Errors: {}'.format(directory_config['first_name']['empty']['err_msg']))
            elif row['Last_Name'] == '' or row['Last_Name'] == ' ':
                # Adding a column for error with custom error message 'empty' from json
                import_result.diff.append('Errors: {}'.format(directory_config['last_name']['empty']['err_msg']))

        return import_result

    # skip_row method is to skip the records those are satisfying some specific conditions
    def skip_row(self, instance, original):
        # custom exceptions which will help to skip the current record, conditions included are,
        # 1. Email_Address should not be empty
        # 2. Subjects_Taught should not be more than 5
        # 3. First name and Last_Name should not be blank
        if (instance.Email_Address == '' or instance.Email_Address == ' ') or \
                len(instance.Subjects_Taught.split(',')) > directory_config['subject_taught']['limit'] or \
                (instance.First_Name == '' or instance.First_Name == ' ') or \
                (instance.Last_Name == '' or instance.Last_Name == ' '):
            # return True will advises the Resource class to skip the current record
            # False is to include the record; which is default value
            return True

    class Meta:
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        model = Teacher

# Admin class to control the admin page
class TeacherAdmin(ImportExportModelAdmin):

    resource_class = ModelResource

    # table fields to display in the admin page
    list_display = ('First_Name', 'Last_Name', 'Email_Address', 'Phone_Number', 'Room_Number', 'Subjects_Taught')
    # search fields for the admin page
    search_fields = ('First_Name', 'Last_Name', 'Email_Address', 'Phone_Number', 'Subjects_Taught')

    # applying filters in the admin page
    list_filter = [FirstLetterFilter, ]

# registering the Model and ModelAdmin class
admin.site.register(Teacher, TeacherAdmin)
