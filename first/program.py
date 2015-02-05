#coding=utf-8
#!/usr/bin/env python
import paramiko
import socket
from multiprocessing.dummy import Pool as ThreadPool


class Serverscreate():
    statusCode = {
        '0': '验证成功',
        '1': '安装成功',
        '2': '安装错误',
        '3': '无法连接',
        '4': '认证失败',
        '5': '密码错误',
    }

    def verify(self, servers):
        ip = servers[0]
        username = servers[1]
        password = servers[2]

        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.connect(ip, 22, username, password, timeout=5)
            s.close()
            print 'Status is ok!'
            code = '0'
            status = self.statusCode[code]

        except socket.error, e:
            print 'Socket connection failed:', e
            code = '3'
            status = self.statusCode[code]
        except paramiko.AuthenticationException:
            print 'Authentication failed for some reason'
            code = '4'
            status = self.statusCode[code]
        except paramiko.SSHException, e:
            print 'Password is invalid:', e
            code = '5'
            status = self.statusCode[code]

        return ip, status, code

    def install(self, servers):
        ip = servers[0]
        username = servers[1]
        password = servers[2]
        script = servers[3]

        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            s.connect(ip, 22, username, password, timeout=5)

            t = paramiko.Transport((ip, 22), )
            t.connect(username=username, password=password)

            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(script, script)

            cmd = "sh " + script
            print cmd

            stdin, stdout, stderr = s.exec_command(cmd)

            print '{} is running the scripts'.format(ip)

            out = stdout.read()
            err = stderr.read()

            s.close()

            print err

            f = open(ip + '_log', 'w')
            f.write(out)
            f.close()

            if err:
                f = open(ip + 'err', 'w')
                f.write(err)
                f.close()
                code = '2'
                status = self.statusCode[code]
            else:
                code = '1'
                status = self.statusCode[code]

            print '{} finished the script'.format(ip)

        except socket.error, e:
            print 'Socket connection failed:', e
            code = '3'
            status = self.statusCode[code]
        except paramiko.AuthenticationException:
            print 'Authentication failed for some reason'
            code = '4'
            status = self.statusCode[code]
        except paramiko.SSHException, e:
            print 'Password is invalid:', e
            code = '5'
            status = self.statusCode[code]

        return ip, status, code