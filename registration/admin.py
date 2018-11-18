from django.contrib import admin
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