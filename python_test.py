import paramiko 

sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy)

server = "10.231.249.13"
user = "root"
pwd = "ldcc!2626"
port = 22 

sshClient.connect(server, port, username=user, password=pwd) 
stdin,stdout,stderr = sshClient.exec_command("ls -al /tbbackup/archive_backup_dest/*.arc | wc -l")
lines = stdout.readlines()

archive_cnt = ''.join(lines) 
print ("운영 통합 DB1 Backup Archive Cnt : " + archive_cnt)
#print (''.join(lines))


cmd = '''
. .bash_profile && tbsql -s sys/dbaakstp << EOF 
set term off
set head off
set feed off
select to_char(max(time),'YYYY-MM-DD HH24:MI:SS') as backup_time ,status,
       count(*)
from v\$backup     
group by status;
EOF
'''

stdin,stdout,stderr = sshClient.exec_command(cmd)
#err = stderr.readlines()
#print(err)
lines = stdout.readlines()

backup_status = ''.join(lines) 

print(backup_status)
sshClient.close()
