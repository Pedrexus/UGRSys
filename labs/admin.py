from django.contrib import admin
from .models import Waste, Laboratory, Department, BookmarkedWaste

admin.site.register(Waste)
admin.site.register(Laboratory)
admin.site.register(Department)
admin.site.register(BookmarkedWaste)
