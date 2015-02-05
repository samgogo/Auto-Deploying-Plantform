#!/usr/bin/env python
import paramiko
import socket
import os, sys
import getpass
from multiprocessing import Process, Lock

class Createservers:
    def menu(self):
        menu = raw_input('\nAdd:(a), Edit:(e), Delete(d), Show All(s),Verify All(v), Install(i), Quit(q) ').strip().lower()
        return menu

    def editServer(self, menu):
        if menu == 'a':
            print 'add a server'
            ip = raw_input('Please type the ip address ').strip()
            if ip in serversList:
                print 'The Server is already in the list!'
            else:
                username = raw_input('username: ').strip()
                password = getpass.getpass('password: ')
                while True:
                    types = ('gate', 'logic', 'db')
                    serverType = raw_input('server type? (gate, logic, DB)')
                    if serverType.strip().lower() in types:
                        break
                    else:
                        continue
                script = files[serverType.lower()]
                serversList[ip] = {'username': username, 'password': password, 'script': script}

        if menu == 'd':
            print 'Remove a server.'
            ip = raw_input('Please type the ip address ').strip()
            if ip in serversList:
               del serversList[ip]
               print 'Server {} has been removed'.format(ip)
            else:
               print 'server {} not found!'.format(ip)

        if menu == 'e':
            print 'Edit a server'
            ip = raw_input('Please type the ip address ').strip()
            if ip in serversList:
                username = raw_input('username: ').strip()
                password = getpass.getpass('password: ')
                while True:
                    types = ('gate', 'logic', 'db')
                    serverType = raw_input('server type? (gate, logic, DB)')
                    if serverType.strip().lower() in types:
                        break
                    else:
                        continue
                script = files[serverType.lower()]
                serversList[ip] = {'username': username, 'password': password, 'script': script}
            else:
                print 'server {} not found!'.format(ip)

    def showServers(self, serverList):
        print '\nServers that will be setup as follows:'
        if serversList != {}:
            for ip in serverList:
                script = serverList[ip]['script']
                print '\n{}: {}'.format(ip, script)
        else:
            print 'No server has been found!'

    def showServersStatus(self, ip, username, password, script, lock):
        lock.acquire()
        if serversList != {}:
            print '\n{}: {}'.format(ip, script)
            #check server status
            try:
                s = paramiko.SSHClient()
                s.load_system_host_keys()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(ip, 22, username, password, timeout=5)
                s.close()
                print 'Status is ok!'
            except paramiko.SSHException, e:
                print 'Password is invalid:', e
            except paramiko.AuthenticationException:
                print 'Authentication failed for some reason'
            except socket.error, e:
                print 'Socket connection failed:', e
        else:
            print 'No server has been found!'
        lock.release()

    def execFile(self, ip, username, password, script):
        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            t = paramiko.Transport((ip, 31819))
            t.connect(username=username, password=password)

            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(script, script)

            cmd = "sh " + script

            s.connect(ip, 22, username, password, timeout=5)
            stdin, stdout, stderr = s.exec_command(cmd)

            print '{} is running the scripts'.format(ip)
            print stdout.read()
            print '{} has been setup'.format(ip)

            s.close()

        except paramiko.SSHException, e:
            print 'Password is invalid:', e
        except paramiko.AuthenticationException:
            print 'Authentication failed for some reason'
        except socket.error, e:
            print 'Socket connection failed:', e


if __name__ == "__main__":
    files = {
    'gate': 'gate-systemOptimization-ctl.sh',
    'logic': 'logic-systemOptimization-ctl.sh',
    'db': 'DB-systemOptimization-ctl.sh',
    }

    serversList = {}

    clear = os.system('clear')

    C = Createservers()

    while True:
        A = C.menu()
        if A == 'a':  #add a server
            C.editServer(A)
        elif A == 'e':   #edit a server
            C.editServer(A)
        elif A == 'd':   #delete a server
            C.editServer(A)
        elif A == 's':   #show all servers
            C.showServers(serversList)
        elif A == 'v':   #verify all servers
            print '\nChecking servers status...'
            record = []
            lock = Lock()
            for ip in serversList:
                username = serversList[ip]['username']
                password = serversList[ip]['password']
                script = serversList[ip]['script']
                p = Process(target=C.showServersStatus, args=(ip, username, password, script, lock))
                p.start()
                record.append(p)
            for p in record:
                p.join()
            print 'ok'
        elif A == 'i':   #run scripts on servers
            record = []
            for ip in serversList:
                username = serversList[ip]['username']
                password = serversList[ip]['password']
                script = serversList[ip]['script']
                p = Process(target=C.execFile, args=(ip, username, password, script))
                p.start()
                record.append(p)
            for p in record:
                p.join()
        elif A == 'q':   #quit
            print 'Good Bye'
            sys.exit(0)
