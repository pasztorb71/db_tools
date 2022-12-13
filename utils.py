from tabulate import tabulate


def password_from_file(puser, phost, pport):
    pass_out = ''
    with open('../db_passw.txt', 'r') as f:
        for line in f.read().split('\n'):
            if line.startswith('#'):
                continue
            user, host, port, passw = line.split()
            if '_service' in puser and '_service' in user:
                pass_out = passw
                break
            if host == phost and port == str(pport) and user == puser:
                pass_out = passw
                break
    return pass_out

def print_sql_result(d, maxlength, header=False):
    for db, records in sorted(d.items()):
        print(f"{db}:".ljust(maxlength))
        if records:
            if isinstance(records, str):
                print(f"  {records}")
            else:
                if header and isinstance(records[0], list):
                    print(tabulate(records[1:], headers=records[0], tablefmt="pipe"))
                    print()
                else:
                    #print(f"records: {records}")
                    for value in records:
                        print('  ' + value)
    print(f'Összesen: {len(d)} db repo')
