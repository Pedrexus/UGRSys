from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from registration.models import MyUser


class GeneratorListFilter(admin.SimpleListFilter):
    '''Human-readable title which will be displayed in the
    right admin sidebar just above the filter options.'''
    title = _('Gerador')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'generator'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = model_admin.get_queryset(request)
        generators = set(MyUser.objects.get(user=waste.generator) for waste in queryset)
        options = (
            (str(generator.user), str(generator)) for generator in generators
        )
        return (
                ((None, _('All')),) + tuple(options)
        )

    # Isso impede que a opção "Todos" apareça duas vezes no filtro.
    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() is None:
            return queryset.all()
        else:
            return queryset.filter(generator__username=self.value())

