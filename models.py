from django.db import models
from jsonfield import JSONField
"""
Models for Squid_api.
"""
"""
example of JSON in aclrule.values:

{"values":[
   "192.168.0.0/24",
   "127.0.0.0/24"
]
}

EVERY RECORD IN DATABASE HAVE TO BE IN THIS FORM!
"""


class AclRule(models.Model):
    acl_type = models.CharField(max_length=200, default='foobar')
    acl_values = JSONField(default='NULL')
    acl_name = models.CharField(max_length=200, default='foobar')


class AclList(models.Model):
    id = models.IntegerField(primary_key=True)
    deny_value = models.BooleanField(default=True)
    list_type = models.CharField(max_length=200, default='http_access')
#    acl_rules = models.ManyToManyField(AclRule, through='AccessPattern', through_fields=('acl_rules', 'acl_list'))
    acl_rules = models.ManyToManyField(AclRule)

