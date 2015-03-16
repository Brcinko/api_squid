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
    # f = open('squid.conf', w)
    # f.write(update)
    # f.close()


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


def update_authentication():

    pass


def generate_file(flag_patterns, flag_rules, data_rules, data_patterns, inputfile):
    # Make tmp file with acl rules
    os.remove('/home/brcinko/squid_done.conf')
    with open("/home/brcinko/squid_done.conf.tmp1", "wt") as fout:
        with open(inputfile, "rt") as fin:
            for line in fin:
                fout.write(line.replace(flag_rules, data_rules))
                # fout.write(line.replace(flag_patterns, data_patterns))
    # Add acl patterns to http_access
    with open("/home/brcinko/squid_done.conf.tmp2", "wt") as fout:
        with open("/home/brcinko/squid_done.conf.tmp1", "rt") as fin:
            for line in fin:
                # fout.write(line.replace(flag_rules, data_rules))
                fout.write(line.replace(flag_patterns, data_patterns))
    # TODO add acl of authentification and configuration of auth

    os.remove("/home/brcinko/squid_done.conf.tmp1")


def main():

    rules = update_config_rules()
    patterns = update_config_list()
    generate_file("# INSERT PATTERNS #", "# INSERT RULES #", rules, patterns, '/home/brcinko/squid.conf')


if __name__ == "__main__":
    main()