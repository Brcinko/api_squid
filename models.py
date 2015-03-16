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


class Authentication(models.Model):
    # user database settings
    # explanation of this settings can be found at http://www.squid-cache.org/Versions/v3/3.2/manuals/basic_db_auth.html
    username_column = models.CharField(default="username")
    password_column = models.CharField(default="password")
    database_name = models.CharField(default="squid")
    user = models.CharField()  # database account
    password = models.CharField()  # database account
    table = models.CharField(default="users")
    encryption = models.CharField(default="plaintext")  # password encryption in db, only plaintext or md5
    # squid auth settings
    # explanation of this settings can be found at http://www.squid-cache.org/Doc/config/auth_param/
    realm = models.CharField()
    children = models.IntegerField(default=5)
    program = models.CharField(default="")
    case_sensitive = models.BooleanField(default=False)
    credentialsttl = models.IntegerField(default=4)
    utf8 = models.BooleanField(default=False)