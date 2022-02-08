from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from local.models import *
from django.core import serializers
from django.utils import timezone
from datetime import datetime
import requests
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
@csrf_exempt
def login(request,userid,tokenid,gpsX,gpsY,address):
    try:
        userdata=user_table.objects.get(userID=userid)
        userdata.tokenID=tokenid
        userdata.address=address
        userdata.save()        
        return redirect('/map/'+gpsX+'/'+gpsY)

    except user_table.DoesNotExist:
        userdata=user_table()
        userdata.userID=userid
        userdata.tokenID=tokenid
        userdata.imageUrl='https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png'
        userdata.nickname='이름을 입력해주세요'
        userdata.kakaochat='카카오 오픈 채팅을 입력해주세요'
        userdata.joindate=datetime.today()
        userdata.kakaoID="0"
        userdata.messageonoff="1"
        userdata.address=address
        userdata.save()
        
        return redirect('/map/'+gpsX+'/'+gpsY)

def index(request,gpsX,gpsY):
    context={
        "gpsX":gpsX,
        "gpsY":gpsY,
    }
    return render(request,'mapshow.html',context)

def addr(request,address):
    memodata=gossip_table.objects.filter(address=address).order_by('writeDate')[:20]    
    context=serializers.serialize("json",memodata)    
    return JsonResponse(context,safe=False)

def showAnswer(request,pk): #답변 보여주기
    showAnswer=answer.objects.filter(questionFID=pk).order_by('-writeTime')[:20]
    context=serializers.serialize("json",showAnswer)
    return JsonResponse(context,safe=False)

def inputmemo(request,userid,gpsX,gpsY):    
    context={
        "gpsX":gpsX,
        "gpsY":gpsY,
        "userid":userid,
    }
    return render(request,'memoinput.html',context)

def savememo(request):
    if request.method=='POST':
        saveGossip=gossip_table()
        userData=user_table.objects.get(userID=request.POST['userid'])

        tokendata=user_table.objects.filter(address=userData.address,messageonoff='1').values_list('tokenID')
        ids=[]       
       
        for outstring in tokendata:
            ids.append(outstring[0])
    
        print(ids)

        if(request.POST['kakaoopen']=='open'):
            saveGossip.kakaochat=userData.kakaochat
        else:
            saveGossip.kakaochat="비공개"
        
        saveGossip.gpsX=request.POST['gpsX']
        saveGossip.gpsY=request.POST['gpsY']
        saveGossip.address=request.POST['address']
        saveGossip.memo=request.POST['memo']
        saveGossip.writeDate=timezone.now()
        saveGossip.tokenID=userData.tokenID
        saveGossip.userID=request.POST['userid']
        saveGossip.imageURL=userData.imageUrl
        saveGossip.userFID=userData
        saveGossip.save()                       
        sendSaveMemo(saveGossip.memo,userData.nickname,userData.imageUrl,ids)
    return render(request,'close.html')

def showmemo(request,pk,userid):
    memodata=gossip_table.objects.get(id=pk)
    questiondata=question.objects.filter(gossip=memodata)    
    userdata=user_table.objects.get(userID=userid)
    context={"memodata":memodata,
    "questiondata":questiondata,
    "imageUrl":userdata.imageUrl,
    "uid":userid,}
    return render(request,'showmemo.html',context)

def local(request,address,uid):
    memodata=gossip_table.objects.filter(address=address).order_by('-writeDate')[:20]
    context={"memolist":memodata,
    "uid":uid,}
    return render(request,'local.html',context)

def savequestion(request,pk,questiondata,userid):    
    ids=gossip_table.objects.get(id=pk)
    userdata=user_table.objects.get(userID=userid)
    savedata=question()
    savedata.gossip=ids
    savedata.questiondata=questiondata
    savedata.tokenID=userdata.tokenID
    savedata.userID=userid
    savedata.imageURL=userdata.imageUrl
    savedata.writeTime=timezone.now()
    savedata.save()    
    sendFCM(questiondata,userdata.nickname,userdata.imageUrl,ids.tokenID)
    return HttpResponse('save')

def sendSaveMemo(body,title,imageurl,ids):
    url_send='https://fcm.googleapis.com/fcm/send'    
    apikey ='AAAAMmnv3bM:APA91bF0xJarjfXqUm2aNJwBiSD5zUL_b2IJvcJWHC0eg_neW_5rlxFp_uI7jxhDfUSUEewANCiQ69Y-jfwf4mr91_fMO-orvOJud43aFtAYm_KYVHKdlAjF9DRem_nNi_8lXgDm0J2l'
    headers={
        'Authorization':'key='+apikey,
        'Content-Type':'application/json; UTF-8',
    }    
    content={
        'registration_ids':ids,
        'data':{
            'title':title,
            'message':body,          
            'imageUrl':imageurl,
        },
    }
    result=requests.post(url_send,data=json.dumps(content),headers=headers)    
    return result

def sendFCM(body,title,imageurl,ids):    
    url_send='https://fcm.googleapis.com/fcm/send'    
    apikey ='AAAAMmnv3bM:APA91bF0xJarjfXqUm2aNJwBiSD5zUL_b2IJvcJWHC0eg_neW_5rlxFp_uI7jxhDfUSUEewANCiQ69Y-jfwf4mr91_fMO-orvOJud43aFtAYm_KYVHKdlAjF9DRem_nNi_8lXgDm0J2l'
    headers={
        'Authorization':'key='+apikey,
        'Content-Type':'application/json; UTF-8',
    }
    testids=[ids]    
    content={
        'registration_ids':testids,
        'data':{
            'title':title,
            'message':body,          
            'imageUrl':imageurl,
        },
    }
    result=requests.post(url_send,data=json.dumps(content),headers=headers)    
    return result

def myList(request,userid):
    personallist=gossip_table.objects.filter(userID=userid).order_by('-writeDate')[:40]
    context={
        "personaldata":personallist,
        "uid":userid,
    }
    return render(request,'personallist.html',context)

def statusperson(request,userid):
    return render(request,"status.html",{"uid":userid,})

def saveperson(request):
    userData=user_table.objects.get(userID=request.POST['userid'])
    if(request.POST['name']):
        userData.nickname=request.POST['name']
    if(request.POST['imageurl']):
        userData.imageUrl=request.POST['imageurl']
    if(request.POST['kakao']):
        userData.kakaochat=request.POST['kakao']
    userData.messageonoff=request.POST['notice']
    userData.save()
    return render(request,'close.html')

def homeStatus(request,userid):
    userData=user_table.objects.get(userID=userid)
    context={"person":userData,}
    return render(request,"home.html",context)

def saveAnswer(request,pk,answer_data):
    try:
        answer.objects.get(questionFID=pk)
        return HttpResponse('error')

    except answer.DoesNotExist:
        tokenMassage=question.objects.get(id=pk)
        ansdata=answer()
        ansdata.questionFID=tokenMassage
        ansdata.answerdata=answer_data
        ansdata.writeTime=timezone.now()
        ansdata.save()
        result=sendFCM(answer_data,tokenMassage.questiondata,tokenMassage.imageURL,tokenMassage.tokenID)
        return HttpResponse('save')
