from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,ExpensCreateForm,DateSearchForm,RevieExpensForm
from django.contrib.auth import authenticate,login,logout
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.

def signin(request):
    if request.method=="POST":
            uname=request.POST.get("uname")
            pwd=request.POST.get("password")
            user=authenticate(username=uname,password=pwd)
            if user is not None:
                login(request,user)
                return render(request,"budget/home.html")
            else:
                return render(request, "budget/login.html",{"message":"invalid username or password"})

    return render(request,"budget/login.html")

def registration(request):
    form=UserRegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("user created")
            return redirect("signin")
        else:
            context["form"]=form
            return render(request, "budget/registration.html", context)
    return render(request,"budget/registration.html",context)

def signout(request):
    logout(request)
    return redirect("signin")

@login_required
def expens_create(request):
    form=ExpensCreateForm(initial={'user':request.user})
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ExpensCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addExpens")
        else:
            context["form"]=form
            return render(request, "budget/addexpens.html", context)
    return render(request,"budget/addexpens.html",context)
@login_required
def view_expences(request):
    form=DateSearchForm()
    context={}
    expenses=Expense.objects.filter(user=request.user)
    context["form"]=form
    context["expenses"]=expenses
    if request.method=="POST":
        form=DateSearchForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data.get("date")
            expenses=Expense.objects.filter(date=date,user=request.user)
            context["expenses"]=expenses
            return render(request, "budget/viewexpenses.html", context)
    return render(request,"budget/viewexpenses.html",context)
@login_required
def edit_expens(request,id):
    expens=Expense.objects.get(id=id)
    form=ExpensCreateForm(instance=expens)
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ExpensCreateForm(request.POST,instance=expens)
        if form.is_valid():
            form.save()
            return redirect("viewexpenses")
        else:
            form = ExpensCreateForm(request.POST, instance=expens)
            context["form"]=form
            return render(request, "budget/expenseedit.html", context)
    return render(request,"budget/expenseedit.html",context)


@login_required
def delete_expens(request,id):
    expens=Expense.objects.get(id=id)
    expens.delete()
    return redirect("viewexpenses")



def review_expens(request):
    form=RevieExpensForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=RevieExpensForm(request.POST)
        if form.is_valid():
            from_date=form.cleaned_data.get("from_date")
            to_date=form.cleaned_data.get("to_date")
            total=Expense.objects.filter(date__gte=from_date,date__lte=to_date,user=request.user).aggregate(Sum('amount'))
            total=total["amount__sum"]
            context={
                "form":form,
                "total":total,
            }
            return render(request, "budget/review.html", context)


    return render(request,"budget/review.html",context)