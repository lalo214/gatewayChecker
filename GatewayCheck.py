
import paramiko
from getpass import getpass
import time


def check_gates():
    with open('input.txt') as f:
        ip_list = [x.strip('\n') for x in f]

    username = input('Enter username: ')
    password = getpass()

    for i in range(len(ip_list)):
        ip = (ip_list[i].strip('\n'))

        remote_conn_pre = paramiko.SSHClient()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(ip, port=22, username=username, password=password,
                                look_for_keys=False, allow_agent=False)

        remote_conn = remote_conn_pre.invoke_shell()
        remote_conn.send("en\n")
        remote_conn.send("show ip default-gateway\n")
        time.sleep(.5)

        output = remote_conn.recv(65535).decode('utf-8')

        test_list = output.split()
        for list_iter in range(len(test_list)):
            if '10' in test_list[list_iter] and '.' in test_list[list_iter]:
                print('Management IP:', ip, 'Gateway:', test_list[list_iter])


check_gates()