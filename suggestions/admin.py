from django.contrib import admin

from registration.models import MyUser
from suggestions.models import Suggestion


@admin.register(Suggestion)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'get_user_department',
        'get_user_laboratory',
        'comments',
    )
    empty_value_display = ''
    list_display_links = None

    def get_user_department(self, obj):
        return MyUser.objects.get(user=obj.user).department
    get_user_department.short_description = 'Departamento'


    def get_user_laboratory(self, obj):
        return MyUser.objects.get(user=obj.user).laboratory
    get_user_laboratory.short_description = 'Laboratório'