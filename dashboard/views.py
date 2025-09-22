from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Login_info_new_p,User_posts
from django.contrib import messages
from django.contrib.auth import logout,authenticate
from .forms import UserPostsForm
# Create your views here.
def demo(request):
    posts = User_posts.objects.all().order_by('-create_at')
    users = []
    U_posts = []
    for post in posts:
        log_user = Login_info_new_p.objects.get(email=post.u_name)
        u_name = log_user.fname + log_user.lname
        status = post.post
        U_posts.append(status)
        users.append(u_name)
    return render(request,"dashboard/landing_page.html",{"posts": zip(users,U_posts)})

def register(request):
    return HttpResponse("NEW ACCOUNT CREATED.")

def profile(request):
    S_email = request.session.get('email')
    log_user = Login_info_new_p.objects.get(email=S_email)
    u_name = log_user.fname + log_user.lname
    posts = User_posts.objects.filter(u_name=log_user)
    user_names_post = {}
    for post in posts:
        user_names_post[u_name] = post.post
    
    posts = []
    return render(request,"dashboard/landing_page.html",{"posts": user_names_post})


def login(request):
    if request.session.get('user_id'):
        return redirect("home")
    else:
        if request.method == "POST":
            u_email = request.POST.get("email")
            u_password = request.POST.get("password")
            try:
                logged_user = Login_info_new_p.objects.get(email=u_email,password=u_password)
                request.session['user_id'] = logged_user.id
                request.session["email"] = u_email
                request.session["name"] = logged_user.lname
                
                return redirect("home")
            except:
                messages.error(request,"Invalid")
                return redirect("register") 
        else:
            return render(request,"dashboard/login_signup.html",{})
    
    
def logout_view(request):
    logout(request)
    return redirect("login")

def add_post(request):
    if request.method == "POST":
        form = UserPostsForm(request.POST)
        
        if form.is_valid():
            # return HttpResponse("Post Added Successfully.")
            post = form.save(commit=False)
            post.u_name = Login_info_new_p.objects.get(email=request.session.get('email'))
            post.save()
            return redirect("home")
    else:
        form = UserPostsForm()
    return HttpResponse("Post Was not Added.")