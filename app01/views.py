from django.shortcuts import render,HttpResponse,redirect
import django.http

from app01.models import UserInfo,UserBirthday
from django import forms

class UserBirthForm(forms.ModelForm):
    class Meta:
        model = UserBirthday
        fields = ["name","birthday","isLunar"]

class LoginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
        )
    password = forms.CharField(
        label="密码",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
        )


#---#
def info_main(request):
    return render(request, 'info_main.html')
#---#

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html",{'form':form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_object = UserInfo.objects.filter(name = form.cleaned_data['username'], password = form.cleaned_data['password']).first()
        
        if not user_object:
            form.add_error("username", "用户名错误")
            form.add_error("password", "密码错误")
            return render(request, "login.html",{'form':form})

        request.session["info"] = {'id':user_object.id, 'name':user_object.name}
        return redirect('http://127.0.0.1:8000/info/main')
    


#---#
def info_list(request):
    #get all datas in sql
    data_list = UserInfo.objects.all()
    
    #tansform into html and return
    return render(request,"info_list.html",{"data_list":data_list})

def info_add(request):
    if request.method == "GET":
        return render(request, 'info_add.html')
    
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")

    UserInfo.objects.create(name = user, password = pwd)
    return redirect("http://127.0.0.1:8000/info/list/")

def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id = nid).delete()
    return redirect("http://127.0.0.1:8000/info/list/") 

def info_edit(request, nid):
    if request.method == "GET":
        row_object = UserInfo.objects.filter(id = nid).first()
        return render(request, 'info_edit.html', {"row_object":row_object})
    
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    UserInfo.objects.filter(id=nid).update(name=user)
    UserInfo.objects.filter(id=nid).update(password=pwd)

    return redirect("http://127.0.0.1:8000/info/list/")

#---#

def birth_list(request):
    #get all datas in sql
    data_list = UserBirthday.objects.all()
    
    #tansform into html and return
    return render(request,"birth_list.html",{"data_list":data_list})

def birth_add(request):
    if request.method == "GET":
        form = UserBirthForm()
        return render(request, 'birth_add.html', {"form":form})
    
    form = UserBirthForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("http://127.0.0.1:8000/birth/list/")
    else:
        return render(request, 'birth_add.html', {"form":form})

def birth_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id = nid).delete()
    return redirect("http://127.0.0.1:8000/birth/list/") 

def birth_edit(request):
    return