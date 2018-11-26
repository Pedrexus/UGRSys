from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from registration.models import MyUser


class GeneratorListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
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
        generators = set(MyUser.objects.get(user=evaluation.waste.generator) for evaluation in queryset)
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
            return queryset.filter(
                waste__generator__username=self.value())


class DepartmentListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Departamento')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = model_admin.get_queryset(request)
        departments = set(
            MyUser.objects.get(user=evaluation.waste.generator).department for evaluation in
            queryset)
        options = (
            (str(department), str(department)) for department in departments
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
            my_users_list = MyUser.objects.filter(department__name=self.value())
            usernames_list = [my_user.user.username for my_user in my_users_list]
            return queryset.filter(waste__generator__username__in=usernames_list)


class LaboratoryListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Laboratório')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'laboratory'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        queryset = model_admin.get_queryset(request)
        laboratories = set(
            MyUser.objects.get(user=evaluation.waste.generator).laboratory for evaluation in
            queryset)
        options = (
            (str(laboratory), str(laboratory)) for laboratory in laboratories
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
            my_users_list = MyUser.objects.filter(laboratory__name=self.value())
            usernames_list = [my_user.user.username for my_user in my_users_list]
            return queryset.filter(
                waste__generator__username__in=usernames_list)
