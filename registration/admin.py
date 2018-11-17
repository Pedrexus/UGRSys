from django.contrib import admin
from django.contrib.auth.models import Group

from registration.models import MyUser

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