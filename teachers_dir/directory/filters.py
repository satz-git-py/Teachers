from django.contrib.admin import SimpleListFilter

class FirstLetterFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'First Letter'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'letter'
    letters = list(string.ascii_uppercase)

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        lookups = []
        for letter in self.letters:
            count = qs.filter(name__istartswith=letter).count()
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
            return queryset.filter(name__istartswith=self.value())
