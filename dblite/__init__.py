import sqlite3
import os


def create():
    try:
        already_exists = os.path.exists("template.db")
        conn = sqlite3.connect("template.db")
        conn.row_factory = sqlite3.Row
        if already_exists:
            return conn

        c = conn.cursor()
        from people import CREATE_SCRIPT as PEOPLE_CREATE_SCRIPT
        from session import CREATE_SCRIPT as SESSION_CREATE_SCRIPT
        from company import CREATE_SCRIPT as COMPANY_CREATE_SCRIPT
        from brand import CREATE_SCRIPT as BRAND_CREATE_SCRIPT
        from template import CREATE_SCRIPT as TEMPLATE_CREATE_SCRIPT
        from rules import CREATE_SCRIPT as RULES_CREATE_SCRIPT
        from rules import CREATE_INDEX_SCRIPT as RULES_CREATE_INDEX_SCRIPT
        c.execute(SESSION_CREATE_SCRIPT)
        c.execute(PEOPLE_CREATE_SCRIPT)
        c.execute(COMPANY_CREATE_SCRIPT)
        c.execute(BRAND_CREATE_SCRIPT)
        c.execute(TEMPLATE_CREATE_SCRIPT)
        c.execute(RULES_CREATE_SCRIPT)
        c.execute(RULES_CREATE_INDEX_SCRIPT)
        c.close()
        return conn
    except Exception as ex:
        print '%s' % ex
        raise

