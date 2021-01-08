#!/usr/bin/env python3

import paramiko
import json, sys, os, csv
import socket

# Global vartiables!
username = 'crestron'
password = ''

commands = []
devices = []
shutoff = False
update = False
remotePath = ''

sshclient = paramiko.SSHClient()
sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# def upload_puf():
#   sshclient.connect('100.112.100.230', username='crestron', password='')
#   stdin, stdout, stderr = sshclient.exec_command('dir romdisk/user/system')
#   print(stdout.read().decode('utf-8'))
#   clientftp = sshclient.open_sftp()
  
#   localFile = os.path.join(os.path.dirname(__file__), 'cp3n_1.601.0050.puf')

  # try:
  #   clientftp.put(localFile, 'firmware/cp3n_1.601.0050.puf', confirm=True)
  # except Exception as e:
  #   print(e)
  #   clientftp.close()
  #   sshclient.close()
  #   sys.exit(0)

  # remotepath = clientftp.listdir('firmware')
  # print(remotepath)

  # clientftp.close()
  # sshclient.close()


def shut_port_down(cmd):

  if cmd != 'ctpconsole':
    off_command = cmd + ' off'
  else:
    off_command = cmd + ' disable'
  
  stdin, stdout, stderr = sshclient.exec_command(off_command)
  output = stdout.read().decode('UTF-8').split('\n')[0]
  return output

def runcommands():
  
  for ip in devices:
    
    try:
      sshclient.connect(ip, username=username, password=password, auth_timeout=5, timeout=5)
      
    except paramiko.ssh_exception.NoValidConnectionsError:
      print(f'Unable to connect to {ip}')
      continue
    except socket.timeout:
      print(f'Socket timed out on {ip}')
      continue
    except paramiko.ssh_exception.SSHException as se:
      print(f'SSHException caught: {se}')
      continue
    except Exception as e:
      print(f'Exception unhandled in Connect Method: {e}')
      continue


    for cmd in commands:
      # print(f'{cmd} > {ip}')

      try:
        stdin, stdout, stderr = sshclient.exec_command(cmd)
        output = stdout.read().decode('UTF-8').split('\n')[0]
        # print(output)

        if cmd == 'telnet' or cmd == 'ftpserver' or cmd == 'ctpconsole':
          output = output.split(':')[1]
          if 'Disabled' in output:
            print(f'[{ip}] {cmd.title()} Port already disabled')
          else:
            print(f'[{ip}] {cmd.title()} Port is currently active')
            if shutoff:
              print(f'[{ip}] Disabling {cmd}...')
              result = shut_port_down(cmd)
              print(result)
        
        elif cmd == 'webserver':
          if shutoff:
            print('Shutting off webserver, not yet implemented')
          else:
            print(f'[{ip}] {cmd.title()} Port is on')
          

        elif cmd == 'host':
          output = output.split(':')[1].strip()
          print(output)
        elif cmd == 'ver':
          print(output)
        
        
      except paramiko.SSHException:
        print(f'Command Exec Exception to {ip}')
      except expression as e:
        print(f'Exception thrown: {e}')

    sshclient.close()
    
      

if __name__ == "__main__":
  usage = '''
  usage: python3 main.py [option] <filename>.csv [flag(optional)]
  -v, --version - get version of devices provided into the csv file
  -ch, --check-ports - gets the status of ports, returns if the port is on/off for webserver, ftpserver, ctpconsole, telnet
  -cl, --close-ports - close ports if they are on/enabled for ftpserver, ctpconsole, telnet
  -a, --adhoc - run a command adhoc
  '''

  args = sys.argv

  # WiP for updating systems that are not on the latest firmware
  if len(args) < 3:
    print("Please provide an option for the scan and filename")
    print(usage)
    sys.exit(0)
  elif len(args) == 4:
    if args[3] == 'all' and (args[1] == '--close-ports' or args[1] == '-cl'):
      shutoff = True
    elif args[3] == 'update':
      update = True
    elif (args[1] == '--adhoc' or args[1] == '-a') and args[3]:
      commands = args[3]
    else:
      print(f'{args[3]} is not an option')
      print(usage)
      sys.exit(0)

  try:
    with open(args[2], 'r') as csv_file:
      reader = csv.reader(csv_file)

      for row in reader:
        devices.append(row[0])

  except FileNotFoundError:
    print('File %s does not exist' % args[2])
    sys.exit(0)

  if args[1] == '--version' or args[1] == '-v':
    if update is True:
      # commands = ['ver', 'puf -d']
      print(f'Not yet implemented, if puf file is loaded to multiple devices, it will run the puf -d command to update')
      sys.exit(0)
    else:
      commands = ['ver']
    runcommands()
  elif (args[1] == '--adhoc' or args[1] == '-a') and args[3]:
    runcommands()
  elif args[1] == '--close-ports' or args[1] == '-cl':
    if shutoff is True:
      commands = ['ftpserver', 'telnet', 'ctpconsole', 'webserver']
      user_reply = input('Are you sure you want to shutdown the webserver, you will lose web connectivity to the processor [y/n]')
      if user_reply.lower() == 'n' or user_reply.lower() == 'no':
        print('Exiting...')
        sys.exit(0)
      
      runcommands()

    else:
      shutoff = True
      commands = ['ftpserver', 'telnet', 'ctpconsole']
      runcommands()

  elif args[1] == '--check-ports' or args[1] == '-ch':
    commands = ['ftpserver', 'telnet', 'ctpconsole', 'webserver']
    runcommands()

  else:
    print(f'{args[1]} is not an option')
