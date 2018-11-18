from django.contrib import admin
from django.contrib.auth.models import Group
from labs.models import Waste
from labs.reports import csv_view
from registration.models import MyUser

def export_as_csv(modeladmin, request, queryset):
    gen = queryset.get()
    data = Waste.objects.filter(generator=gen)

    return csv_view(request, data)

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    actions = [export_as_csv, ]




admin.site.unregister(Group)


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'full_name',
        'department',
        'laboratory',
        'email',
        'phone_number',
        'last_login'
    )
    list_display_links = None

    list_filter = ('department', 'laboratory')

    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = 'Último acesso'
