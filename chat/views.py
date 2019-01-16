from django.shortcuts import render
from django.shortcuts import HttpResponse
from chat.models import UserGroup,User
import json,queue
# Create your views here.
Global_Queue = {};
def index(request):
    contact_list = User.objects.filter(friends=int(request.COOKIES.get('uid',None))).values();
    group_list = User.objects.get(pk=int(request.COOKIES.get('uid',None)));
    group_list = group_list.groups.all();
    all_people = User.objects.all().values();
    return render(request,'chatIndex.html',locals());

def login(request):
    if request.is_ajax():
        result = User.objects.filter(username=request.POST['username'],password=request.POST['password']).values()[0];
        if not result:
            response = {
                'flag':False,
                'message':'用户不存在!',
                'errorCode':-1,
            }
            return HttpResponse(response);
        response = {
            'EventType':'signin',
            'flag':True,
            'message':'登陆成功',
            'username':result['username'],
            'uid':result['id'],
        }
    return HttpResponse(json.dumps(response));

def reg(request):
    if request.is_ajax():
        result = User.objects.filter(username=request.POST['username'], password=request.POST['password']);
        if not result:
            #user not reg
            obj = User.objects.create(username=request.POST['username'],password=request.POST['password']);
        return HttpResponse(result.values());
    return HttpResponse('not ok');

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

def sendMsg(request):
    response = {};
    if request.is_ajax():
        uid = int(request.COOKIES.get('uid',None));
        if uid:
            if uid not in Global_Queue.keys():
                Global_Queue[uid]={};
            fid = int(request.POST['to']);
            print(dir(Global_Queue[uid]))
            if fid not in Global_Queue[uid].keys():
                Global_Queue[uid][fid]=queue.Queue();
                Global_Queue[uid][fid].put(request.POST['msg']);
            response['EventType']='sendMsg';
            response['flag']=True;
            print('currentMsgCount:',Global_Queue[uid][fid].qsize())
    return HttpResponse(json.dumps(response))

def getMsg(request):
    response={};
    uid = int(request.COOKIES.get('uid',None));
    d = dict()
    for item in Global_Queue[uid].keys():
        response[item]=Global_Queue[uid][item].qsize();
    response = json.dumps(response);
    return HttpResponse(response);