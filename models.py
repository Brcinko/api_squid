from django.db import models
from jsonfield import JSONField


class AclRules(models.Model):

    acl_type = models.CharField(max_length=200, default='foobar')
    acl_values = JSONField(default='NULL')
    acl_name = models.CharField(max_length=200, default='foobar')

#    def __unicode__(self):              # __unicode__ on Python 2
#        return self



