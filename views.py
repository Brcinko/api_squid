from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_squid.models import AclRule, AclList, Authentication, AuthenticationDB
from api_squid.serializers import AclRuleSerializer, AclListSerializer, AuthenticationSerializer, AuthenticationDBSerializer, AclVersionSerializer
from api_squid.helpers import update_rules, update_list, generate_file, update_authentication
from settings import *


def index(request):
    return Response("This is a index web page of squid API.")


@csrf_exempt
@api_view(['GET', 'POST'])
def acl_rules_list(request):
    """
    Get list of all acl-rules, or create a new acl-rule.
    acl rule contains: 
        acl_name - CharField
        acl_type - CharField - just one of these acl-elements: http://wiki.squid-cache.org/SquidFaq/SquidAcl#ACL_elements 
        acl_values - JSON - have to be in this json form:
            {"values":[
               "192.168.0.0/24",
               "127.0.0.0/24"
            ]
            }
    Allowed method:
        GET  - response to this method return rest_framework Response with list of all serialized acl rules stored in DB
        POST - response to this method save new acl rule into db and return rest_framework Response with serialized record
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def acl_rule_detail(request, pk):
    """
    Detail of specific acl-rule
    Allowed methods:
        GET    - response to this method return rest_framework Response with serialized data of specific acl-rule
        DELETE - response delete specific acl-rule from DB and return rest_framewor Response with code 204
        PUT    - response to this method change specific acl-rule in DB and 
                 return rest_framewrok Response with serialized data of specific acl-rule
    Params: request - requested data
            pk - ID of specific record
    For more info about requested data try OPTIONS on yourdomain.com/api_squid/acl_rules/
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def acl_list(request):
    """
    Get list all acl-lists, or create a new acl-list.
    acl-list contains: 
        id         - Integer (PK)
        acl_rule   - acl_rule obj
        deny_value - Boolean 
        list_type  - CharField - only "http_acces" is allowed
    Allowed method:
        GET  - response to this method return rest_framework Response with list of all serialized acl-lists stored in DB
        POST - response to this method save new acl rule into db and return rest_framework Response with serialized record
    Params: request - requested data
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def acl_list_detail(request, pk):
    """
    Detailed view of one access pattern
    Allowed methods:
        GET    - response to this method return rest_framework Response with serialized data of specific acl-list
        DELETE - response delete specific acl-list from DB and return rest_framework Response with code 204
        PUT    - response to this method change specific acl-list in DB and 
                 return rest_framewrok Response with serialized data of specific acl-list
    Params: request - requested data
            pk - ID of specific record
    For more info about requested data try OPTIONS on yourdomain.com/api_squid/acl_list/
    """
    try:
        pattern = AclList.objects.get(pk=pk)
    except AclRule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AclRuleSerializer(pattern)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = AclRuleSerializer(pattern, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pattern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def authentication(request):
    """
    Get list of all authentication settings, or create a new one
    authentication contains: 
        realm             - CharField
        children          - Integer
        enabled           - Boolean 
        program           - Charfield 
        case_sensitive    - Boolean
        credentialsttl    - Integer
        utf8              - Boolean
        authentication_db - authentication_db obj
        Explanation of parameters: http://www.squid-cache.org/Doc/config/auth_param/
    Allowed method:
        GET  - response to this method return rest_framework Response with list of all serialized acl-lists stored in DB
        POST - response to this method save new acl rule into db and return rest_framework Response with serialized record
    Params: request - requested data
    """
    if request.method == 'GET':
        auth = Authentication.objects.all()
        serializer = AuthenticationSerializer(auth, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def authentication_detail(request, pk):
    """
    Detailed view of one authentication parame record
    Allowed methods:
        GET    - response to this method return rest_framewrok Response with serialized data of specific auth params
        DELETE - response delete specific auth params and return rest_framewor Response with code 204
        PUT    - response to this method change specific auth params in DB and 
                 return rest_framewrok Response with serialized data of specific auth params
                 
    Params: request - requested data
            pk - ID of specific record
    For more info about requested data try OPTIONS on yourdomain.com/api_squid/authentication/
    """
    try:
        auth = Authentication.objects.get(pk=pk)
    except Authentication.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthenticationSerializer(auth)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = AuthenticationSerializer(auth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
def authentication_db(request):
    """
    List of all database settings for authentication
    authenticationDB contains: 
        username_column - CharField
        password_column - CharField
        database_name   - CharField 
        user            - Charfield 
        password        - Charfield
        credentialsttl  - Charfield
        table           - Charfield
        encryption      - Charfield - only "md5" or "plaintext"
        Explanation of parameters: http://www.squid-cache.org/Versions/v3/3.2/manuals/basic_db_auth.html
    Allowed method:
        GET  - response to this method return rest_framework Response with list of all serialized acl-lists stored in DB
        POST - response to this method save new acl rule into db and return rest_framework Response with serialized record
    Params: request - requested data
    """
    if request.method == 'GET':
        db = AuthenticationDB.objects.all()
        serializer = AuthenticationDBSerializer(db, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = AuthenticationDBSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def authentication_db_detail(request, pk):
    """
    Detailed view of specific record of authentification database settings
    Allowed methods:
        GET    - response to this method return rest_framewrok Response with serialized data of specific user DB
        DELETE - response delete specific user DB record and return rest_framewor Response with code 204
        PUT    - response to this method change specific user DB record in DB and 
                 return rest_framewrok Response with serialized data of specific user DB
    
    Params: request - requested data
            pk - ID of specific record
    For more info about requested data try OPTIONS on yourdomain.com/api_squid/authentication_db/
    """
    try:
        db = AuthenticationDB.objects.get(pk=pk)
    except AuthenticationDB.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthenticationDBSerializer(db)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # data = JSONParser().parse(request)
        serializer = AuthenticationDBSerializer(db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        db.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'PUT'])
def update_config(request):
    """
    Generating squid.conf file from database
    Allowed methods:
        GET    - response to this method generate new config file of Squid proxy and ad new version of acl-lists into DB
    
    Params: request - requested data
    """
    if request.method == 'GET':  # TODO method will be PUT?
        auth = Authentication.objects.latest('id')
        rules = AclRule.objects.all()
        patterns = AclList.objects.all()

        # # Update acl rules declarations
        generate_file(rules, patterns, auth, SQUID_ORIGIN_FILE)
        data = []
        for p in patterns:
            data.append(p.id)
        ver = {}
        vers = {'acl_lists': data}
        # return Response(vers)

        version_serializer = AclVersionSerializer(data=vers)
        if version_serializer.is_valid():
            version_serializer.save()
            return Response(version_serializer.data, status=status.HTTP_201_CREATED)
        return Response(version_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


