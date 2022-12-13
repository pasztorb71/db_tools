import multiprocessing

import psycopg2

from utils import password_from_file


def parallel_run(ports, databases, func):
    global jobs
    host = 'localhost'
    return_dict = multiprocessing.Manager().dict()
    jobs = []
    for port in ports:
        for db in databases[0:]:
            p = multiprocessing.Process(target=func, args=(host, port, db, return_dict))
            jobs.append(p)
            p.start()
    # Wait until all process finish
    for job in jobs:
        job.join()
    return return_dict

def mproc_single_command_tmpl(host, port, db, return_dict):
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=db,
        user="postgres",
        password=password_from_file('postgres', host, port))
    cur = conn.cursor()
    cur.execute("SELECT schemaname, tablename, tableowner FROM pg_tables WHERE tableowner NOT IN ('cloudsqladmin') AND schemaname NOT IN ('public')")
    record = cur.fetchall()
    return_dict[db] = [[desc[0].upper() for desc in cur.description]] + record
    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    databases = ['core_notification_wa']
    #ports = list(range(5433,5440))
    ports = [5432]
    return_dict = parallel_run(ports, databases, mproc_single_command_tmpl)
    pass
    #print_sql_result(return_dict, len(max(databases, key=len)) + 5, header=True)