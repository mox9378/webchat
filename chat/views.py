from django.shortcuts import render
from django.shortcuts import HttpResponse
from chat.models import UserGroup,User,Messages
import json,queue,datetime
from copy import deepcopy
from django.db.models import Q
# Create your views here.
Global_Queue = dict();
def index(request):
    contact_list,group_list,all_people=None,None,None;
    if request.COOKIES.get('is_logind',None):
        contact_list = User.objects.filter(friends=int(request.COOKIES.get('uid',None))).values();
        group_list = User.objects.get(pk=int(request.COOKIES.get('uid',None)));
        group_list = group_list.groups.all();
        all_people = User.objects.all().values();
    return render(request,'chatIndex.html',locals());

def login(request):
    if request.is_ajax():
        result = User.objects.filter(username=request.POST['username'],password=request.POST['password']).values();
        if result:
            result = result[0];
        else:
            result={};
        if not result:
            response = {
                'EventType': 'signin',
                'flag':False,
                'message':'用户不存在!',
                'errorCode':-1,
            }
            return HttpResponse(json.dumps(response));
        response = {
            'EventType':'signin',
            'flag':True,
            'message':'登陆成功',
            'username':result['username'],
            'uid':result['id'],
            'user':result['user']
        }
    return HttpResponse(json.dumps(response));

def reg(request):
    if request.is_ajax():
        response = dict();
        response['flag'] = False;
        response['EventType'] = 'signup';
        response['message'] = 'register error!';
        result = User.objects.filter(username=request.POST['username']); #, password=request.POST['password']
        if not result:
            #user not reg
            obj = User.objects.create(user=request.POST['user'],username=request.POST['username'],password=request.POST['password']);
            obj.groups.add(UserGroup.objects.get(pk=100000));
            #obj.save()
            response['flag']=True;
            response['message']='register success';
    return HttpResponse(json.dumps(response));

def reFresh(request):
    contact_list = User.objects.filter(friends=int(request.COOKIES.get('uid',None))).values();
    obj = User.objects.get(pk=int(request.COOKIES.get('uid',None)));
    group_list = obj.groups.all().values();
    people_list = User.objects.all().values();
    response = {
        'EventType':'refresh',
        'contact_list':list(contact_list),
        'group_list':list(group_list),
        'people_list':list(people_list)
    }
    return HttpResponse(json.dumps(response));


def pushMsg(msg_t):
    if not Global_Queue.get(msg_t['fid']):
        Global_Queue[msg_t['fid']] = queue.Queue();
    Global_Queue[msg_t['fid']].put_nowait(msg_t);
    return;

def sendMsg(request):
    #优化结构
    response={};
    response['EventType']='sendMsg';
    response['flag']=False;

    msg_t = {};
    if request.is_ajax():
        #for ajax request
        uid = int(request.POST.get('uid',None));
        fid = int(request.POST.get('fid',None));
        msg = str(request.POST.get('msg', None)).strip();
        msgid = int(request.POST.get('msgid', None));
        EventType = int(request.POST.get('EventType', None));
        msg_t = {
            'pk': uid + fid,
            'uid': uid,
            'fid': fid,
            'msg': msg,
            'msgid': msgid,
            'c_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        };
        if uid and fid and msg:
            if(EventType==0): # 0 == People msg
                uname = User.objects.get(pk=uid);
                response['msgid'] = msgid;
                response['message'] = msg_t;
                response['flag'] = True;
                msg_t['EventType']=0;
                msg_t['user']=uname.user;
                print(msg_t['uid'], ' sender to: ', msg_t['fid'], ' msg: ', msg_t['msg']);
                pushMsg(msg_t);
            else: # 1 == group msg
                gid = UserGroup.objects.get(pk=msg_t['uid']);
                member_list = list(gid.user_set.all().values('id'));
                msg_t['EventType'] = EventType;
                uname = User.objects.get(pk=fid);
                msg_t['user'] = uname.user;
                for i in member_list:
                        msg_t['fid'] = i['id'];
                        msg_t['ffid']=fid;
                        msg_t['pk']=msg_t['fid'] + msg_t['uid'];
                        print(msg_t['uid'], ' sender to: ', msg_t['fid'], ' msg: ',msg_t['msg']);
                        pushMsg(deepcopy(msg_t));
                response['message'] = '';
                response['flag'] = True;
        return HttpResponse(json.dumps(response,cls=priJsonEncoder));
    else:
        response['message']=request.POST;
        return HttpResponse(json.dumps(response,cls=priJsonEncoder));

def getMsg(request):
    if request.is_ajax():
        response={};
        response['EventType'] = 'getMsg';
        response['flag']=False;
        response['message']='';
        uid = int(request.COOKIES.get('uid', None));
        if not Global_Queue.get(uid,None):
            Global_Queue[uid]=queue.Queue();
        while True:
            try:
                tmp = Global_Queue[uid].get(timeout=60);
                response['message'] = tmp;
                response['flag'] = True;
                break;
            except queue.Empty:
                break;
    return HttpResponse(json.dumps(response,cls=priJsonEncoder));

def addUser(request):
    uid = int(request.COOKIES.get('uid',None));
    fid = int(request.POST.get('fid',None));
    if uid and fid and fid != uid:
        response = {};
        rFlag = User.objects.get(pk=uid);
        res = [i[0] for i in rFlag.friends.all().values_list('id')]
        if rFlag:
            if fid in res:
                response['flag'] = 0;
            else:
                response['flag'] = 1;
                rFlag.friends.add(User.objects.get(pk=fid));
    return HttpResponse(json.dumps(response));


class priJsonEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S');
        else:
            json.JSONEncoder.default(self,o);