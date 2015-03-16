from django.contrib import admin
from api_squid.models import AclRule, AclList, Authentication, AuthenticationDB
# Register your models here.


class AclListAdmin(admin.ModelAdmin):
    fields = ('deny_value', 'acl_rules', 'list_type', 'id')

admin.site.register(AclRule)
admin.site.register(AclList, AclListAdmin)
admin.site.register(Authentication)
admin.site.register(AuthenticationDB)


