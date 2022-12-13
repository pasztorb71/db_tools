
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