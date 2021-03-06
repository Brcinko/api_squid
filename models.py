from django.db import models
from jsonfield import JSONField
"""
    Models for Squid_api.
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
    acl_values = models.CharField(max_length=10000, default='NULL')
    acl_name = models.CharField(max_length=200, default='foobar', unique=True)


class AclList(models.Model):
    id = models.IntegerField(primary_key=True)
    deny_value = models.BooleanField(default=True)
    list_type = models.CharField(max_length=200, default='http_access')
#   acl_rules = models.ManyToManyField(AclRule, through='AccessPattern', through_fields=('acl_rules', 'acl_list'))
    acl_rules = models.ManyToManyField(AclRule)


class AclVersion(models.Model):
#    ver = models.IntegerField(primary_key=True)
    acl_lists = models.ManyToManyField(AclList)
    ver = models.AutoField(primary_key=True)


class AuthenticationDB(models.Model):
    """
        DB model of "Database of users" for squid_db_auth helper
        explanation of this settings can be found at http://www.squid-cache.org/Versions/v3/3.2/manuals/basic_db_auth.html
        or here: http://manpages.ubuntu.com/manpages/precise/man8/squid3_db_auth.8.html
        Warning:
            Default settings of database_name are set on localhost database with name "squid". If you want use
            another database database_name have to be in this form:
            "host=my_host_or_ip;port=port_number;database=database_name"
    """
    username_column = models.CharField(default="username", max_length=200, null=True)
    password_column = models.CharField(default="password", max_length=200, null=True)
    database_name = models.CharField(default="host=localhost;database=squid", max_length=200, null=True)
    user = models.CharField(max_length=200)  # database account
    password = models.CharField(max_length=200)  # database account
    table = models.CharField(default="users", max_length=200, null=True)
    encryption = models.CharField(default="plaintext", max_length=200, null=True)  # password encryption in db only plaintext or md5


class Authentication(models.Model):
    """
        DB model of Squid authentication parameters
        explanation of this settings can be found at http://www.squid-cache.org/Doc/config/auth_param/
    """
    realm = models.CharField(max_length=200, default="Squid Authentication", null=True)
    children = models.IntegerField(default=5, null=True)
    program = models.CharField(default="/usr/local/squid/libexec/squid_db_auth", max_length=200, null=True)
    case_sensitive = models.BooleanField(default=False)
    credentialsttl = models.IntegerField(default=4, null=True)
    utf8 = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    authenticationdb = models.ForeignKey(AuthenticationDB)