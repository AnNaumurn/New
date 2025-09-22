from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Login_info_new_p
from .models import Comment

def profile_with_comments(request, u_id):
    profile_user = get_object_or_404(Login_info_new_p, id=u_id)
    comments = Comment.objects.filter(profile_owner=profile_user).select_related("author").order_by("-created_at")

    if request.method == "POST":
        my_id = request.session.get("user_id")
        if not my_id:
            return redirect("login")

        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(
                author_id=int(my_id),   # make sure it's an integer
                profile_owner=profile_user,
                text=text
            )
            messages.success(request, "Comment added ✅")
            return redirect("profile_comments", u_id=u_id)

    return render(request, "dashboard/profile_comments.html", {
        "profile_user": profile_user,
        "comments": comments
    })
