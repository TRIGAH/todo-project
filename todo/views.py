from django.contrib.auth.models import User
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .models import Todo
from .forms import TodoForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'todo/home.html')

def signupuser(request):
    if request.method=='GET':
         return render(request,'todo/signupuser.html',{'form':UserCreationForm()}) 
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])  
                user.save()    
                login(request,user)
                return redirect('currenttodos')
            except TypeError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Username already exists'})    
        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Passwords did not match'})    


def loginuser(request):
    if request.method=='GET':
        return render(request,'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(username=request.POST['username'],password=request.POST['password']) 
        if user is None:   
            return render(request,'todo/loginuser.html',{'form':AuthenticationForm(),'error':'Username and Password did not match'})
        else:
            login(request,user)
            return redirect('currenttodos')
    
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return render(request,'todo/home.html') 
@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else:
        form = TodoForm(request.POST)    
        newtodo = form.save(commit=False)
        newtodo.user = request.user  
        newtodo.save() 
        return redirect('currenttodos')

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo/current.html',{'todos':todos})    

@login_required
def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form})    
    else:
       form = TodoForm(request.POST,instance=todo)  
       form.save()
       return redirect('currenttodos')

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user,datecompleted__isnull=True)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')
    else:
        return render(request,'todo/viewtodo.html')  

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk,user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
    else:
        return render(request,'todo/viewtodo.html')   
         
@login_required
def completed(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user,datecompleted__isnull=False)  
        return render(request,'todo/completedtodos.html',{'todos':todos})     
    else:
        pass    


       