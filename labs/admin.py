from django.contrib import admin
from .models import Waste, Laboratory, Department, Substance, SubstanceName

admin.site.register(Waste)
admin.site.register(Laboratory)
admin.site.register(Department)
admin.site.register(Substance)
admin.site.register(SubstanceName)
