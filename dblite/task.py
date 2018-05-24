from dblite import create
from dblite.session import create_session


def insert_table_task(task_id, user_id, info="", task_status='PENDING', result=""):
    connection = create()
    c = connection.cursor()
    c.execute(
        'insert into task (task_id, user_id, status, info, result) values (?,?,?,?,?)',
        (task_id, user_id, task_status, info, result))
    c.close()
    connection.commit()
    connection.close()
    return task_id



def update_table_task(task_id, **kwargs):
    connection = create()
    c = connection.cursor()
    sql = ''
    sql += 'update task set '
    sql += (',').join(k + ' = ?' for k, v in kwargs.iteritems())
    sql += '\twhere task_id = ?'
    params = list(v for k, v in kwargs.iteritems())
    params.append(task_id)
    # params = list(v for k, v in kwargs.iteritems()).append(id)
    print sql
    print params
    c.execute(sql, params)
    c.close()
    connection.commit()
    connection.close()


def delete_task(task_id):
    c = create()
    cur = c.cursor()
    cur.execute("delete from task where task_id = ?", task_id)
    cur.close()
    c.commit()


def get_user_tasks(user_id):
    c = create()
    cur = c.cursor()
    cur.execute("select * from task where user_id = ? and create_date >= date('now')", [user_id])
    rows = cur.fetchall()
    cur.close()
    c.close()
    return [dict(row) for row in rows]


def set_status(task_id, task_status, result=""):
    update_table_task(task_id, status=task_status, result=result)
