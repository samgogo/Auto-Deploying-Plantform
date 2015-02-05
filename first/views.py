#coding=utf-8
from django.shortcuts import render, render_to_response, RequestContext
from multiprocessing.dummy import Pool as ThreadPool
from first.program import Serverscreate

def index(request):
    return render_to_response('index.html')

def serverscreate(request):
    if 'ip' in request.POST:
        ip = request.POST['ip']
        username = request.POST['username']
        password = request.POST['password']
        types = request.POST['types']
        script = ''
        if types == u'网关服务器':
            script = 'gate-systemOptimization-ctl.sh'
        elif types == u'逻辑服务器':
            script = 'logic-systemOptimization-ctl.sh'
        elif types == u'数据库服务器':
            script = 'DB-systemOptimization-ctl.sh'
        request.session[ip] = {
            'username': username,
            'password': password,
            'types': types,
            'script': script,
            'status': 'none',
            'code': ''
        }
        serversList = request.session.items()
    else:
        serversList = request.session.items()
    return render_to_response('serverscreate.html', locals(), context_instance=RequestContext(request))


def serversdelete(request):
    serversList = request.session.items()
    if 'ip' in request.POST:
        ip = request.POST['ip']
        del request.session[ip]
        serversList = request.session.items()
    return render_to_response('serverscreate.html', locals(), context_instance=RequestContext(request))


def serversclear(request):
    request.session.clear()
    serversList = request.session.items()
    return render_to_response('serverscreate.html', locals(), context_instance=RequestContext(request))


def serversverify(request):
    S = Serverscreate()
    servers = []
    pool = ThreadPool(8)
    serversList = request.session.items()

    for ip, info in serversList:
        serversList = request.session.items()
        username = info['username']
        password = info['password']
        server = (ip, username, password)
        # build up servers list to be verified
        servers.append(server)
    # verify servers
    result = pool.map(S.verify, servers)
    pool.close()
    pool.join()

    for ip, status, code in result:
        request.session[ip]['status'] = status
        request.session[ip]['code'] = code

    # update servers' status
    request.session.modified = True
    serversList = request.session.items()

    return render_to_response('serverscreate.html', locals(), context_instance=RequestContext(request))


def serversinstall(request):
    S = Serverscreate()
    servers = []
    pool = ThreadPool(8)
    serversList = request.session.items()

    for ip, info in serversList:
        username = info['username']
        password = info['password']
        script = info['script']
        server = (ip, username, password, script)
        # build up servers list to be verified
        servers.append(server)

    # install servers
    result = pool.map(S.install, servers)
    pool.close()
    pool.join()

    for ip, status, code in result:
        request.session[ip]['status'] = status
        request.session[ip]['code'] = code
    # update servers' status
    request.session.modified = True
    serversList = request.session.items()

    #servers can only be installed once!
    installed = '1'

    return render_to_response('serverscreate.html', locals(), context_instance=RequestContext(request))