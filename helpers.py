__author__ = 'brcinko'

import os
import psycopg2
import psycopg2.extras
import json
import fileinput
from settings import *

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


def update_rules(rules):
    data = ""
    for rule in rules:
        acl_string = ""
        help_acl_string = "acl " + rule.acl_name + " " + rule.acl_type + " "
        for value in rule.acl_values["values"]:
            acl_string += help_acl_string + value + '\n'
        data += acl_string
    return data


def update_list(patterns):
    data = ""
    for pattern in patterns:
        if pattern.deny_value is True:
            pattern_str = "http_access deny "
        else:
            pattern_str = "http_access allow "
        acls_str = ""
        for acls in pattern.acl_rules.all():
            acls_str += acls.acl_name + " "
        data += pattern_str + acls_str + "\n"

    return data


def get_db_string(db):
    db_string = '  --dsn "DSN:mysql:host=localhost;database=' + db.database_name + '" '
    db_string += '--user ' + db.user + ' --password ' + db.password + ' --table'  + db.table
    db_string += ' --usercol ' + db.username_column + ' --passwdcol ' + db.password_column + ' --' + db.encryption
    db_string += "\n"

    return db_string


def update_authentication(auth):
    db_string = get_db_string(auth.authenticationdb)
    if auth.enabled is not False:
        auth_string = "auth_param basic program " + auth.program + db_string
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
            auth_string += "auth_param basic utf8 off" + " \n"
        return auth_string
    else:
        return False


def generate_file(data_rules, data_patterns, data_auth, inputfile):
    auth_str = update_authentication(data_auth)
    rules_str = update_rules(data_rules)
    patterns_str = update_list(data_patterns)

    flag_patterns = "# INSERT PATTERNS #"
    flag_rules = "# INSERT RULES #"

    # Make tmp file with acl rules
    # os.remove('/home/brcinko/squid_done.conf')
    with open("/home/brcinko/squid_done.conf.tmp1", "wt") as fout:
        with open(inputfile, "rt") as fin:
            for line in fin:
                fout.write(line.replace(flag_rules, rules_str))

    # Add acl patterns to http_access
    with open("/home/brcinko/squid_done.conf.tmp2", "wt") as fout:
        with open("/home/brcinko/squid_done.conf.tmp1", "rt") as fin:
            for line in fin:
                fout.write(line.replace(flag_patterns, patterns_str))
    if auth_str is not False:
        with open("/home/brcinko/squid_done.conf.tmp3", "wt") as fout:
            with open("/home/brcinko/squid_done.conf.tmp2", "rt") as fin:
                for line in fin:
                    fout.write(line.replace("# AUTH PARAM #", auth_str))
        with open("/home/brcinko/squid_done.conf.tmp4", "wt") as fout:
            with open("/home/brcinko/squid_done.conf.tmp3", "rt") as fin:
                for line in fin:
                    fout.write(line.replace("# AUTH ACL #", "acl api_auth proxy_auth REQUIRED"))
        with open("/home/brcinko/squid_done.conf", "wt") as fout:
            with open("/home/brcinko/squid_done.conf.tmp4", "rt") as fin:
                for line in fin:
                    fout.write(line.replace("# AUTH PATTERN #", "http_access allow db-auth"))

    os.remove("/home/brcinko/squid_done.conf.tmp1")
    os.remove("/home/brcinko/squid_done.conf.tmp2")
    if auth_str is not False:
        os.remove("/home/brcinko/squid_done.conf.tmp3")
        os.remove("/home/brcinko/squid_done.conf.tmp4")
    else:
        os.rename("/home/brcinko/squid_done.conf.tmp2", "/home/brcinko/squid_done.conf")


def main():

    #rules = update_config_rules()
    #patterns = update_config_list()
    #generate_file( rules, patterns, auth , '/home/brcinko/squid.conf')
    update_authentication(auth)

if __name__ == "__main__":
    main()