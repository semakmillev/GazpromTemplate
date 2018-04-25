import sqlite3
#from people import CREATE_SCRIPT
import os




def create():
    try:
        already_exists = os.path.exists("user.db")
        conn = sqlite3.connect("user.db")
        if already_exists:
            return conn

        c = conn.cursor()
        from dblite.session import CREATE_SCRIPT as SESSION_CREATE_SCRIPT
        c.execute(SESSION_CREATE_SCRIPT)
        c.close()
        return conn
    except Exception as ex:
        print '%s' % ex
        raise
