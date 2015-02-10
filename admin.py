from django.contrib import admin
from api_squid.models import AclRule, AclList
# Register your models here.


class AclListAdmin(admin.ModelAdmin):
    fields = ('deny_value', 'acl_rules', 'id')

admin.site.register(AclRule)
admin.site.register(AclList, AclListAdmin)


