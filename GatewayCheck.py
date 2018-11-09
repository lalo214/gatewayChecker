import socket
import paramiko
from getpass import getpass
import time

# open file of IP's to SSH into
with open('input.txt') as f:
    ip_list = [x.strip('\n') for x in f]

# need loop for exception handling
login_invalid = True
while login_invalid:
    username = input('Enter username: ')
    password = getpass()

    # iterate through list of IPs to SSH to each one
    for i in range(len(ip_list)):
        ip = (ip_list[i].strip('\n'))
        # attempt to connect to SSHClient
        try:
            remote_conn_pre = paramiko.SSHClient()
            remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            remote_conn_pre.connect(ip, timeout=3, port=22, username=username, password=password,
                                    look_for_keys=False, allow_agent=False)
        except paramiko.AuthenticationException:
            print("Authentication failed. Please verify credentials: ")
            break

        except paramiko.SSHException:
            print("Unable to establish SSH connection to:", ip)
            continue
        # exception required for timeout errors
        except socket.error:
            print("Unable to establish SSH connection to:", ip)
            continue

        login_invalid = False
        remote_conn = remote_conn_pre.invoke_shell()
        # commands sent to CLI
        remote_conn.send("en\n")
        remote_conn.send("show ip default-gateway\n")
        time.sleep(.5)
        output = remote_conn.recv(65535).decode('utf-8')

        # print out the IP and it's default gateway
        test_list = output.split()
        for list_iter in range(len(test_list)):
            # data cleaning 
            if '10' in test_list[list_iter] and '.' in test_list[list_iter]:
                print('Management IP:', ip, 'Gateway:', test_list[list_iter])
