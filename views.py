from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_squid.models import AclRule, AclList
from api_squid.serializers import AclRuleSerializer, AclListSerializer


def index(request):
    return HttpResponse("This is a index web page of squid API.")

#
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['GET', 'POST'])
def acl_rules_list(request):
    """
    List of all acl-rules, or create a new acl-rule.
    """
    if request.method == 'GET':
        rules = AclRule.objects.all()
        serializer = AclRuleSerializer(rules, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = AclRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def acl_rule_detail(request, pk):
    """
    Detail of specific acl-rule
    """
    try:
        rule = AclRule.objects.get(pk=pk)
    except AclRule.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AclRuleSerializer(rule)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = AclRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rule.delete()
        return HttpResponse(status=HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def acl_list(request):
    """
    List all acl-lists, or create a new acl-list.
    """
    if request.method == 'GET':
        acl_lists = AclList.objects.all()
        serializer = AclListSerializer(acl_lists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = AclRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def acl_list_detail(request, pk):
    """
    Detailed view of one access pattern
    """
    try:
        pattern = AclList.objects.get(pk=pk)
    except AclRule.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AclRuleSerializer(pattern)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = AclRuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pattern.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)



