from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_null(value):
    if value == null or value ==' ':
        print('empty column')
        # raise ValidationError(
        #     _('%(value)s is not an even number'),
        #     params={'value': value},
        # )