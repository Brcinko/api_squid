from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from api_squid.models import AclRules
# Create your views here.

from api_squid.serializers import AclRulesSerializer


def index(request):
    return HttpResponse("This is a index web page of squid API.")


def rules_list(request):
    acl_rules_list = AclRules.objects.all()
    # output = ', '.join([p.aclrules for p in acl_rules_list])
    # tmp = AclRules()
    acl_list = ""
    for rule in acl_rules_list:
        acl_list += str(rule.id) + " "
        acl_list += str(rule.acl_type) + " "
        acl_list += str(rule.acl_values) + " "
        acl_list += str(rule.acl_name)
        acl_list += "\n"
    return HttpResponse(acl_list)


def acl_rule(request, aclrules_id):
    response = "You're looking at the results of acl rule %s."
    return HttpResponse(response % aclrules_id)

# Check if urls.py works


def skuska(request):
    return HttpResponse("SKUSKA.")


class AclRulesViewSet(viewsets.ModelViewSet):

    queryset = AclRules.objects.all()
    serializer_class = AclRulesSerializer