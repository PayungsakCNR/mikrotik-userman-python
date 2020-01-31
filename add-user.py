'''
Python Script for read personal user data from .csv and add to Mikrotik Userman by SSH method.
Payungsak Klinchampa
Network Engineer
Next-Hop Co., Ltd.
'''
import paramiko
import csv
import secrets
import string
from datetime import datetime

### simple username patten by firstname and lastname ###
def genUserName(firstname,lastname):
    return str(firstname.lower() + "." + lastname[0].lower())

### Generate password function ###
def genUserPassword(len):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(len))
    return password

with open('user-list.csv') as csv_file:
    start=datetime.now()

    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    ### Set SSH Parameter ###
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="my-tik.example.com",port=22,username="admin",key_filename="/path/to/private-key.pem")
    
    ### Write Heading (room,firstname,lastname,tel,password) ###
    with open('user-list-with-password.csv', mode='a+') as userAndPassFile:
        userAndPassFile = csv.writer(userAndPassFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        userAndPassFile.writerow(['room', 'firstname', 'lastname', 'tel', 'username' , 'password'])

    for row in csv_reader:
        ### get personal data from user-list.csv and add to userman ###
        userName  = genUserName(row[1],row[2])
        userPassword = genUserPassword(6)
        stdin , stdout , stderr = ssh.exec_command('tool user-manager user add' + ' username=' + userName + ' password=' + userPassword + ' customer="admin"' + ' copy-from="user00" ' + ' first-name=' + row[1] + ' last-name=' + row[2] + ' phone=' + row[3] + ' location=' + row[0])
        
        print (stdout.read())
        ### get personal data from user-list.csv and write into user-list-with-password.csv ###
        with open('user-list-with-password.csv', mode='a+') as userAndPassFile:
                userAndPassFile = csv.writer(userAndPassFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                userAndPassFile.writerow([row[0], row[1], row[2], row[3], userName, userPassword])
        line_count += 1
    
    ssh.close() ## Close SSH Connection ##
    
    ## Print number of users processed and processed time ##
    print(f'\nProcessed {line_count-1} users.')
    print ("Processed Time: " + str(datetime.now()-start))
