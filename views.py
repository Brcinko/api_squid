from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api_squid.models import AclRule, AclList
from api_squid.serializers import AclRuleSerializer, AclListSerializer


def index(request):
    return HttpResponse("This is a index web page of squid API.")


# def acl_rule(request, aclrule_id):
#     response = "You're looking at the results of acl rule %s."
#     return HttpResponse(response % aclrule_id)


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
        rules = AclRule.objects.all()
        serializer = AclRuleSerializer(rules, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AclRuleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def acl_rule_detail(request, pk):
    """
    Detail of specific acl-rule
    """
    try:
        rule = AclRule.objects.get(pk=pk)
    except AclRule.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AclRuleSerializer(rule)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AclRuleSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


@csrf_exempt
def acl_list(request):
    """
    List all acl-lists, or create a new acl-list.
    """
    if request.method == 'GET':
        acl_lists = AclList.objects.all()
        serializer = AclListSerializer(acl_lists, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AclListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def acl_list_detail(request, pk):
    """
    Detailed view of one access pattern
    """
    try:
        pattern = AclList.objects.get(pk=pk)
    except AclRule.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AclRuleSerializer(pattern)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AclListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

