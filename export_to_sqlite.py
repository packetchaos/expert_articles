import sqlite3
from sqlite3 import Error
from tenable.io import TenableIO

access_key = 'ACCESS_KEY_GOES_HERE'
secret_key = 'SECRET_KEY_GOES_HERE'

tio = TenableIO(access_key, secret_key, vendor='Casey Reid', product='Export into SQLite', build='0.0.1')


def new_db_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as sql_error:
        print(sql_error)
    return conn


def db_query(statement):
    database = r"TENB.db"
    query_conn = new_db_connection(database)
    with query_conn:
        cur = query_conn.cursor()
        cur.execute(statement)

        data = cur.fetchall()
    query_conn.close()
    return data


def insert_vulns(conn, vulns):
    sql = '''INSERT or IGNORE into vulns(
                            asset_uuid, 
                            output, 
                            plugin_id, 
                            plugin_name, 
                            port
    ) VALUES(?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute('pragma journal_mode=wal;')
    cur.execute(sql, vulns)


def create_vulns_table():
    database = r"TENB.db"
    vuln_conn = new_db_connection(database)
    vuln_table = """CREATE TABLE IF NOT EXISTS vulns (
                            asset_uuid text,  
                            output text, 
                            plugin_id text, 
                            plugin_name text,  
                            port text
                            );"""
    vuln_conn.execute(vuln_table)


def export():
    database = r"TENB.db"
    vuln_conn = new_db_connection(database)

    create_vulns_table()
    with vuln_conn:
        for vulns in tio.exports.vulns():

            asset_uuid = vulns['asset']['uuid']
            port = vulns['port']['port']
            plugin_id = vulns['plugin']['id']
            plugin_name = vulns['plugin']['name']

            try:
                output = vulns['output']
            except KeyError:
                output = None

            data_list = [asset_uuid, output, plugin_id, plugin_name, port]

            insert_vulns(vuln_conn, data_list)

export()

#print(db_query("select count(*) from vulns;"))

