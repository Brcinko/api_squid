__author__ = 'brcinko'

import os
import psycopg2
import psycopg2.extras
import json

"""
This code update squids configuration file
TODO update_config_list() for acl_list
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
                    data += row['acl_name'] + " " + row['acl_type'] + " "
                    data += v + "\n"
        results = []

    print data
    # f = open('squid.conf', w)
    # f.write(update)
    # f.close()


def main():
    update_config_rules()


if __name__ == "__main__":
    main()