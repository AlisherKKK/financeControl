import psycopg2
import config as cfg

conn = None


def connect():
    """ Connect to the PostgreSQL database server """
    global conn
    try:
        params = cfg.config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def check_user(uid, fn, nm):
    global conn
    if conn == None:
        connect()
    cur = conn.cursor()
    cur.execute(f'select count(*) from users where id={uid}')
    if int(cur.fetchone()[0]) == 0:
        cur.execute(
            f"insert into users(id, fullname,log_date, nickname) values({uid}, '{fn}', now(), '{nm}'); commit;")
    cur.close()


def get_ctg(uid, incomefl):
    global conn
    if conn == None:
        connect()
    cur = conn.cursor()
    exec_sql = f'select c.code, c.descr from user_categories uc, category c where uc.user_id={uid} and uc.category_id=c.id';
    if incomefl in (0, 1):
        exec_sql = f'{exec_sql} and c.incomefl={incomefl}'
    cur.execute(exec_sql)
    ctgrs = []
    cur_row = cur.fetchone()
    while cur_row != None:
        ctgrs.append(list(cur_row))
        cur_row = cur.fetchone()
    cur.close()
    return list(ctgrs)


def add_operation(uid, ct, sm, cm, incfl):
    global conn
    if conn == None:
        connect()

    ct_code = ct[1:]
    ct_desc = ''
    if ' ' in ct or '-' in ct or '/' not in ct:
        ct_code = ct.split('-')[0]
        ct_desc = ct.split('-')[1]

    cur = conn.cursor()
    cur.execute(f"call add_operation({uid}, '{ct_code}', {sm}, '{cm}',{incfl}, '{ct_desc}');commit;")
    cur.close()

