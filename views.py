from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api_squid.models import AclRules
from api_squid.serializers import AclRulesSerializer


def index(request):
    return HttpResponse("This is a index web page of squid API.")


# def acl_rule(request, aclrules_id):
#     response = "You're looking at the results of acl rule %s."
#     return HttpResponse(response % aclrules_id)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def acl_rules_list(request):
    """
    List all code acl-rules, or create a new acl-rule.
    """
    if request.method == 'GET':
        rules = AclRules.objects.all()
        serializer = AclRulesSerializer(rules, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AclRulesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


def acl_rule_detail(request, pk):
    """
    Detail of specific acl-rule
    """
    try:
        rule = AclRules.objects.get(pk=pk)
    except AclRules.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AclRulesSerializer(rule)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AclRulesSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)