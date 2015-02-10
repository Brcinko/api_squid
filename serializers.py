from rest_framework import serializers
from api_squid.models import AclRule, AclList


class AclRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AclRule
        fields = ('id', 'acl_name', 'acl_type', 'acl_values')


class AclListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AclList
        fields = ('id', 'acl_rules', 'deny_value', 'list_type')
