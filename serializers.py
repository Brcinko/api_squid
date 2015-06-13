from rest_framework import serializers
from api_squid.models import AclRule, AclList, Authentication, AuthenticationDB, AclVersion


class AclRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AclRule
        fields = ('id', 'acl_name', 'acl_type', 'acl_values')


class AclListSerializer(serializers.ModelSerializer):
    # acl_rules = AclRuleSerializer(many=True)
    acl_rules = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
        # slug_field='id'
        # queryset=AclRule.objects.get(pk=acl_rules)
    )

    class Meta:
        model = AclList
        fields = ('id', 'acl_rules', 'deny_value', 'list_type')


class AclVersionSerializer(serializers.ModelSerializer):
    # acl_rules = AclRuleSerializer(many=True)
    acl_lists = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=AclList.objects.all()
    )

    class Meta:
        model = AclVersion
        fields = ('acl_lists',)


class AuthenticationDBSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthenticationDB
        fields = ('id', 'username_column', 'password_column', 'database_name', 'user', 'password', 'table', 'encryption')


class AuthenticationSerializer(serializers.ModelSerializer):
    authenticationdb = AuthenticationDBSerializer(many=False, read_only=True)

    class Meta:
        model = Authentication
        fields = ('id', 'realm', 'children', 'program', 'case_sensitive', 'credentialsttl', 'utf8', 'enabled', 'authenticationdb')


