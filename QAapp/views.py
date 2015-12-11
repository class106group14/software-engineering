# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import User
from django import forms


# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


def register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            User.objects.create(username=username, password=password)
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
            user = User.objects.filter(username__exact=username, password__exact=password)
            if not user:
                return HttpResponseRedirect('/login/')
            else:
                request.session['username'] = username
                return HttpResponseRedirect('/question/')
    else:
        userform = UserForm()
    return render_to_response('login.html', {'userform': userform})


def logout(request):
    session = request.session.get('username', False)  # if get user
    if session:
        del request.session['username']
        return render_to_response('logout.html', {'username': session})
    else:
        return HttpResponse('please login!')  # 未登录


def question(request):  # question match，search best answer,as aan answer save, to showaswer
    # if request.POST:
    #   ques = request.POST['ques']
    return render_to_response('question.html')  # showanswer


def showanswer(request):  # q,a1,a2

    return render_to_response('showanswer.html')


def editanswer(request):  # t.all answer,edit answer，increase answer zzz
    return render_to_response('editanswer.html')


def questionlist(request):  # question zzz
    return render_to_response('questionlist.html')  # question_lst


def answerlist(request):
    return render_to_response('answerlist.html')


def answer(request):  # answer input keyword,search some question
    return render_to_response('answer.html')  # ,{'ques_lst': ques_lst}


def givescore(request):  # which answer score xs

    return render_to_response('showanswer.html')


# def manage(request):#user question qudiao

#    return render_to_response('managepage.html')

def managepage(request):  # zengjia quanxian lw
    if request.method == 'POST':
        ads = request.POST["pass"]
        if ads == "admin":
            User.limit = 1
            return render_to_response('managepage.html')


def manageout(request):  # quxiao quanxian lw
    User.limit = 1
    return render_to_response('question.html')


def userlist(request):  # lw
    user_lst = User.objects.all()
    if user_lst[0].username:
        return render_to_response('userlist.html', {'user_lst': user_lst})
    else:
        return render_to_response('managepage.html')


def deluser(request):  # which answer score lw
    if 'id' in request.GET:
        n_user_lst = User.objects.filter(username=request.GET['id'])
        n_user_lst.delete()
    user_lst = User.objects.all()
    return render_to_response('userlist.html', {'user': user_lst})


def delquestion(request):  # which answer score xs

    return render_to_response('message.html')


def delanswer(request):  # which answer score xs

    return render_to_response('message.html')  # keyi fanhui guanliyemian chakanquanxian
