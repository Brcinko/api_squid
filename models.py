from django.db import models
from jsonfield import JSONField


class AclRule(models.Model):
    acl_type = models.CharField(max_length=200, default='foobar')
    acl_values = JSONField(default='NULL')
    acl_name = models.CharField(max_length=200, default='foobar')


# def __unicode__(self):              # __unicode__ on Python 2
#        return acl_rules_text


class AclList(models.Model):
    id = models.IntegerField(primary_key=True)
    deny_value = models.BooleanField(default=True)
#    acl_rules = models.ManyToManyField(AclRule, through='AccessPattern', through_fields=('acl_rules', 'acl_list'))
    acl_rules = models.ManyToManyField(AclRule)

#
# class AccessPattern(models.Model):
#     acl_rules = models.ForeignKey(AclRule)
#     acl_list = models.ForeignKey(AclList)