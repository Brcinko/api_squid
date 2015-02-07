from rest_framework import serializers
from api_squid.models import AclRules, AclList


class AclRulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AclRules
        fields = ('id', 'acl_name', 'acl_type', 'acl_values')


#class AclListSerializer(serializers.ModelSerializer):

 #   class Meta:
  #      model = AclList
   #     fields = ('id', 'rules', 'deny_value')
