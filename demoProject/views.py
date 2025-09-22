from django.http import HttpResponse
from django.shortcuts import redirect,render


def homepage(request):
    return HttpResponse("hello")

def login(request):
    if request.method == "POST":
        name = request.POST.get("email")
        password = request.POST.get("password")
        pass_from_database = "12345"
        if password == pass_from_database:
            return HttpResponse("WELCOME TO Dashboard "+name+"  "+password)
        return redirect("login")
    else:
        return render(request,"dashboard/login_signup.html",{})

def profile(request,u_id):
    
    return HttpResponse("WELCOME TO Login "+str(u_id))