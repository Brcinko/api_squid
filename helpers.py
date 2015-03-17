__author__ = 'brcinko'

import os
import psycopg2
import psycopg2.extras
import json
import fileinput

"""
This file contains method to update a reconfigure squid proxy server
"""
"""
example of JSON in aclrule.values:

{"values":[
   "192.168.0.0/24",
   "127.0.0.0/24"
]
}

EVERY RECORD IN DATABASE HAVE TO BE IN THIS FORM!
"""

columns = (
    'acl_values'
)


def database_connect():
    # TODO try catch block
    conn_string = "host='localhost' dbname='squid_api' user='squid' password='Passw0rd'"
    connection = psycopg2.connect(conn_string)
    # return connection.cursor()
    return connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def update_config_rules():
    cursor = database_connect()
    # TODO try chatch block
    cursor.execute("SELECT * FROM api_squid_aclrule")
    rows = cursor.fetchall()
    data = ""
    results = []
    for row in rows:
        name = row["acl_name"]
        results.append(dict(zip(columns, row)))
        for value in results:

            jsonstring = value["l"]
            j = json.loads(jsonstring)
            for v in j["values"]:
                if row['acl_name'] == name:
                    data += "acl " + row['acl_name'] + " " + row['acl_type'] + " "
                    data += v + "\n"
        results = []

    return data


def update_config_list():
    cursor = database_connect()
    # TODO try catch block
    cursor.execute('SELECT * FROM api_squid_acllist '
                   'JOIN api_squid_acllist_acl_rules ON api_squid_acllist.id = api_squid_acllist_acl_rules.acllist_id '
                   'JOIN api_squid_aclrule ON api_squid_acllist_acl_rules.aclrule_id = api_squid_aclrule.id '
                   )
    rows = cursor.fetchall()
    pattern = []

    for row in rows:
        help_string = "http_access "
        if row[2] is True:
            help_string += "deny "
        else:
            help_string += "allow "
        list_id = row[0]
        for r in rows:
            if list_id == r[0]:
                help_string += r[10] + " "
        pattern.append(help_string)

    unique_string = ""
    checked = []
    for e in pattern:
        if e not in checked:
            checked.append(e)
            unique_string += e + "\n"
    return unique_string


def update_authentication(auth, adb):
    if auth.enabled is not False:
        auth_string = "auth_param basic program " + auth.program + " \n"
        auth_string += "auth_param basic children " + str(auth.children) + " \n"
        auth_string += "auth_param basic realm " + auth.realm + " \n"
        auth_string += "auth_param basic credentialsttl " + str(auth.credentialsttl) + " \n"
        if auth.case_sensitive is True:
            auth_string += "auth_param basic case_sensitive on" + " \n"
        else:
            auth_string += "auth_param basic case_sensitive off" + " \n"
        if auth.utf8 is True:
            auth_string += " auth_param basic utf8 on" + " \n"
        else:
            auth_string += " auth_param basic utf8 off" + " \n"
        return auth_string
    else:
        return False


def generate_file(data_rules, data_patterns, auth, adb,  inputfile):
    flag_patterns = "# INSERT PATTERNS #"
    flag_rules = "# INSERT RULES #"

    auth_str = update_authentication(auth, adb)
    # Make tmp file with acl rules
    # os.remove('/home/brcinko/squid_done.conf')
    with open("/home/brcinko/squid_done.conf.tmp1", "wt") as fout:
        with open(inputfile, "rt") as fin:
            for line in fin:
                fout.write(line.replace(flag_rules, data_rules))

    # Add acl patterns to http_access
    with open("/home/brcinko/squid_done.conf.tmp2", "wt") as fout:
        with open("/home/brcinko/squid_done.conf.tmp1", "rt") as fin:
            for line in fin:
                # fout.write(line.replace(flag_rules, data_rules))
                fout.write(line.replace(flag_patterns, data_patterns))
    if auth_str is not False:
        with open("/home/brcinko/squid_done.conf.tmp3", "wt") as fout:
            with open("/home/brcinko/squid_done.conf.tmp2", "rt") as fin:
                for line in fin:
                    # fout.write(line.replace(flag_rules, data_rules))
                    fout.write(line.replace("# AUTH PARAM #", auth_str))
    # TODO add acl of authentification and configuration of auth

    os.remove("/home/brcinko/squid_done.conf.tmp1")
    os.remove("/home/brcinko/squid_done.conf.tmp2")


def main():

    #rules = update_config_rules()
    #patterns = update_config_list()
    #generate_file( rules, patterns, auth , '/home/brcinko/squid.conf')
    update_authentication(auth, "")

if __name__ == "__main__":
    main()