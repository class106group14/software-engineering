# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from models import User,Question,Answer,Questionans
import MySQLdb
import difflib
from django import forms

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
          
def register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            User.objects.create(username = username, password = password)
            return HttpResponseRedirect('/login/')
    else:
        userform = UserForm()
    return render_to_response('register.html', {'userform': userform})
          
def login(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = User.objects.filter(username__exact = username, password__exact = password)
            if not user:
                return HttpResponseRedirect('/login/')
            else:
                request.session['username'] = username
                return render_to_response('question.html',{'username':username})
    else:
        userform = UserForm()
    return render_to_response('login.html', {'userform': userform})
          

def logout(request):
    session = request.session.get('username', False)#if get user
    if session:
        del request.session['username']
        return render_to_response('logout.html', {'username': session})
    else:
        return HttpResponse('please login!')#未登录

def question(request):#question match，search best answer,as aan answer save, to showaswer
    username = request.session.get('username')
    return render_to_response('question.html',{'username':username})

def showanswer(request):#q,a1,a2
    if request.POST:
        quest = request.POST['ques']        
        ques_lst = Question.objects.all()
        samelst = [0]*len(ques_lst)
        queslst = [0]*len(ques_lst)#wenti xiangsidu
        anslst = [0]*len(ques_lst)
        ans = []#daan zuijia
        ques = []
        for i in range (0,len(ques_lst)):
            samelst[i] = difflib.SequenceMatcher(None, quest, ques_lst[i].question).ratio()#jisuan  xiangsidu
            queslst[i] = samelst[i]         
            ansl = ques_lst[i].answers.all()
            maxlen = 0
            maxindex = 0
            for j in range (0,len(ansl)):
                if len(ansl[j].answer)>maxlen:
                    maxlen = len(ansl[j].answer)
                    maxindex = j
            samelst[i] += maxlen/250#daan de youxianxing
            anslst[i] = maxindex#yigewenti de zuichangdaan
            ans += [ansl[maxindex].answer]
        inda = samelst.index(max(samelst))#zuiyou wenti 
        #wenti chuanguoqu
        for i in range(0,3):#xunhuan 3 ci 
            indq = queslst.index(max(queslst))
            ques += [ques_lst[indq].question]
            queslst[indq] = 0
        
        usern = request.session.get('username')#baoun wenti
        user1 = User.objects.get(username = usern)
        
        if quest in ques_lst:
            multiple_question = Question.objects.get(question = quest)
            user1.myquestions.add(multiple_question)
        else:
            ansbest = Answer.objects.get(answer = ans[inda])
            multiple_answer = Answer(answer = ans[inda],score = ansbest.score)
            multiple_answer.save()
            multiple_question = Question(question = quest)
            multiple_question.save()
            multiple_question.answers.add(multiple_answer)
            user1.myquestions.add(multiple_question)
        return render_to_response('showanswer.html',{'question':quest, 'answer':ans[inda],'queslst':ques})#showanswer
    return render_to_response('showanswer.html')

def quesans(request):
    if 'id' in request.GET:
        quest = request.GET['id']
        #return HttpResponse(quest)
        ques = Question.objects.get(question = quest)
        anslst = ques.answers.all()
        return render_to_response('ques-ans.html',{'question':quest,'answer_lst':anslst})
    #return render_to_response('ques-ans.html')

def editanswer(request):#t.all answer,edit answer，increase answer zzz
    if 'id' in request.GET:
        ques = request.GET['id']
        quest = Question.objects.get(question = ques)
        answer = quest.answers.all()
    return render_to_response('editanswer.html',{'question':ques,'answer_lst':answer})
#增加addanswer、changeanswer函数和链接
def addanswer(request):
    if 'ques' in request.GET:
        ques = request.GET['ques']
        request.session['questiona'] = ques
        #return HttpResponse(chan)
        multiple_question = Questionans(question = ques)
        return render_to_response('addans.html',{'question':multiple_question})
    if request.POST:
        ans = request.POST['answer']
        multiple_answer = Answer(answer = ans,score = 60)
        multiple_answer.save()
        ques = request.session.get('questiona')
        multiple_question = Questionans(question = ques)
        multiple_question.save()
        multiple_question.answers.add(multiple_answer)
        questionall = Question.objects.get(question = ques)#tianjia jin suoyouwenti 
        questionall.answers.add(multiple_answer)
        usern = request.session.get('username')#baoun
        user1 = User.objects.get(username = usern)
        user1.myanswers.add(multiple_question)
        del request.session['questiona']
        messa = '答案添加成功'
        return render_to_response('message.html',{'message':messa})
        
def changeanswer(request):
    if 'origin' in request.GET and 'ques' in request.GET:
        orig = request.GET['origin']
        ques = request.GET['ques']
        request.session['questionc'] = ques
        request.session['ans'] = orig
        #return HttpResponse(chan)
        multiple_answer = Answer.objects.get(answer = orig)
        multiple_question = Questionans(question = ques)
        return render_to_response('changeans.html',{'answer':multiple_answer,'question':multiple_question})
    if request.POST:
        ans = request.POST['answer']
        anso = request.session.get('ans')
        multiple_answer = Answer.objects.get(answer = anso)
        ques = request.session.get('questionc')
        questionall = Question.objects.get(question = ques)#
        questionall.answers.remove(multiple_answer)#yichu yuanlai de 
        multiple_question = Questionans(question = ques)
        if (multiple_question):
            multiple_question.answers.remove(multiple_answer)
        multiple_answer.answer = ans
        multiple_answer.save()
        multiple_question = Questionans(question = ques)#添加到我的回答中
        multiple_question.save()
        multiple_question.answers.add(multiple_answer)
        questionall.answers.add(multiple_answer)
        usern = request.session.get('username')#baoun
        user1 = User.objects.get(username = usern)
        user1.myanswers.add(multiple_question)
        del request.session['ans']
        del request.session['questionc']
        messa = '答案修改成功'
        return render_to_response('message.html',{'message':messa})
        
def changeaddanswer(request):#修改增加
    if 'origin' in request.GET and 'ques' in request.GET:
        orig = request.GET['origin']
        ques = request.GET['ques']
        request.session['questionc'] = ques
        request.session['ans'] = orig
        #return HttpResponse(chan)
        multiple_answer = Answer.objects.get(answer = orig)
        multiple_question = Questionans(question = ques)
        return render_to_response('changeaddans.html',{'answer':multiple_answer,'question':multiple_question})
    if request.POST:
        ans = request.POST['answer']
        anso = request.session.get('ans')
        ques = request.session.get('questionc')
        multiple_answer = Answer.objects.get(answer = anso)
        questionall = Question.objects.get(question = ques)#
        multiple_question = Questionans(question = ques)
        if (multiple_question):
            answers = multiple_question.answers.all()
            if multiple_answer in answers:
                multiple_question.answers.remove(multiple_answer)#之前回答过
                multiple_answer.answer = ans
            else:
                multiple_answer = Answer(answer = ans,score = 60)
        else:
            multiple_answer = Answer(answer = ans,score = 60)
        multiple_answer.save()
        multiple_question = Questionans(question = ques)#添加到我的回答中
        multiple_question.save()
        multiple_question.answers.add(multiple_answer)
        questionall.answers.add(multiple_answer)#添加到所有问题中
        usern = request.session.get('username')#baoun
        user1 = User.objects.get(username = usern)
        user1.myanswers.add(multiple_question)
        del request.session['questionc']
        del request.session['ans']
        messa = '答案修改成功'
        return render_to_response('message.html',{'message':messa})

def questionlist(request):#question zzz
    #if request.GET:
    usern = request.session.get('username')#get name
    user1 = User.objects.get(username = usern)
    queslst = user1.myquestions.all()
    #return HttpResponse(queslst[0].question)
    return render_to_response('questionlist.html',{'question_lst':queslst})#question_lst
    
def mquestionlist(request):
    q_lst = Question.objects.all()
    if q_lst[0]:
        return render_to_response('mquestionlist.html', {'question_lst':q_lst})
    else:
        return render_to_response('managepage.html')
    #
def myanswer(request):
    usern = request.session.get('username')#get name
    user1 = User.objects.get(username = usern)
    queslst = user1.myanswers.all()
    return render_to_response('myanswer.html',{'question_lst':queslst})

def answerlist(request):
    if 'id' in request.GET:
        #usern = request.session.get('username')#get name
        #user1 = User.objects.get(username = usern)
        quest = request.GET['id']#wenti??
        ques = Questionans.objects.get(question = quest)
        anslst = ques.answers.all()
        #return HttpResponse(anslst[0].answer)
    return render_to_response('answerlist.html',{'answer_lst':anslst,'quest':quest})

def answer(request):#answer input keyword,search some question 
    if request.POST:
        key = request.POST['key']
        ques_lst = Question.objects.all()
        queoutlst = []
        samelst = [0]*len(ques_lst)
        for i in range (0,len(ques_lst)):
            samelst[i] = difflib.SequenceMatcher(None, key, ques_lst[i].question).ratio()
            if samelst[i]>0:
                queoutlst += [ques_lst[i].question]
        #return HttpResponse(queoutlst[0])
        return render_to_response('answer.html',{'ques_lst':queoutlst})#,{'ques_lst': ques_lst}
    
    return render_to_response('answer.html')
def givescore(request):#which answer score xs
    if 'id' in request.GET:
        ans = request.GET['id']
        request.session['answer'] = ans
        answer = Answer.objects.get(answer = ans)
        return render_to_response('givescore.html',{'answer':answer})
    if request.POST:
        ans = request.session.get('answer')
        score = request.POST['score']#how to get answer
        answer = Answer.objects.get(answer = ans)
        answer.score = score
        #return HttpResponse(answer.answer)
        answer.save()
        del request.session['answer']
        messa = '评分成功'
        return render_to_response('message.html',{'message':messa})

#def manage(request):#user question qudiao
#    return render_to_response('managepage.html')

def managepage(request):  # zengjia quanxian lw
    usern = request.session.get('username')
    user1 = User.objects.get(username = usern)
    if request.method == 'POST':
        ads = request.POST["pass"]
        if ads == "admin":
            user1.limit = True
            user1.save()
            #user = User(username = user1.username,password = user1.password,myquestions = user1.myquestions,
            #    myanswers = user1.myanswers,limit = False)
            #user.save()
    if user1.limit == True:
        return render_to_response('managepage.html')
    else:
        return render_to_response('question.html',{'username':usern})


def manageout(request):  # quxiao quanxian lw
    usern = request.session.get('username')
    #return HttpResponse(user1.username)
    user1 = User.objects.get(username = usern)
    user1.limit = False
    #user = User(username = user1.username,password = user1.password,myquestions = user1.myquestions,
    #            myanswers = user1.myanswers,limit = False)
    user1.save()
    return render_to_response('question.html',{'username':usern})


def userlist(request):  # lw
    user_lst = User.objects.all()
    if user_lst[0].username:
        return render_to_response('userlist.html',{'user_lst':user_lst})
    else:
        return render_to_response('managepage.html')


def deluser(request):  # which answer score lw
    if 'id' in request.GET:
        n_user_lst = User.objects.filter(username=request.GET['id'])
        n_user_lst.delete()
    user_lst = User.objects.all()
    return render_to_response('userlist.html', {'user_lst': user_lst})

def delquestion(request):#which answer score xs
    if 'id' in request.GET:
        ques = request.GET['id']
        quest = Question.objects.get(question = ques)
        answers = quest.answers.all()#delete answers
        answers.delete()
        quest.delete()
        messa = '操作成功，该项问题已删除'
    return render_to_response('message.html',{'message':messa})

def delanswer(request):#which answer xs
    if 'id' in request.GET:
        ans = request.GET['id']
        answer = Answer.objects.get(answer = ans)
        answer.delete()
        messa = '操作成功，该项答案已删除'
    return render_to_response('message.html',{'message':messa})#keyi fanhui guanliyemian chakanquanxian
