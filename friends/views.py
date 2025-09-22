from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models, transaction
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import friend_list, friend_request
from comments.models import Comment
from dashboard.models import Login_info_new_p


def profile_with_comments(request, u_id):
    """Show a user profile with comments and allow posting new ones"""
    profile_user = get_object_or_404(Login_info_new_p, id=u_id)
    comments = Comment.objects.filter(profile_owner=profile_user).select_related("author")

    if request.method == "POST":
        my_id = request.session.get("user_id")
        if not my_id:
            return redirect("login")

        text = request.POST.get("text", "").strip()
        if text:
            Comment.objects.create(
                author_id=int(my_id),  # make sure it's int
                profile_owner=profile_user,
                text=text
            )
            messages.success(request, "Comment added ✅")
            return redirect("profile_comments", u_id=u_id)

    return render(request, "friends/profile_comments.html", {
        "profile_user": profile_user,
        "comments": comments
    })


def allFriends(request):
    my_id = request.session.get("user_id")
    all_users = Login_info_new_p.objects.all()

    user_data = {u.id: {0: u.email, 1: u.fname, 2: u.lname} for u in all_users}

    friendships = friend_list.objects.filter(user_id=my_id)
    friends_data = []
    for fr in friendships:
        u = fr.friend_id
        friends_data.append({
            "my_id": fr.user_id.id,
            "id": u.id,
            "name": f"{u.fname} {u.lname}",
            "email": u.email,
        })
    return render(request, "friends/friend_list.html", {
        "friends": friends_data,
        "my_id": my_id,  # fix here
        "user_data": user_data
    })


def friend_req(request, u_id):
    my_id = request.session.get("user_id")
    if not my_id:
        return redirect("login")

    if int(my_id) == int(u_id):
        messages.error(request, "You can't send a request to yourself.")
        return HttpResponse("You can't send a request to yourself.")

    user = get_object_or_404(Login_info_new_p, id=my_id)
    friend = get_object_or_404(Login_info_new_p, id=u_id)

    if friend_list.objects.filter(user_id=user, friend_id=friend).exists():
        messages.info(request, "You are already friends.")
        return HttpResponse("You are already friends.")

    if friend_request.objects.filter(
        models.Q(sender_id=user, receiver_id=friend) |
        models.Q(sender_id=friend, receiver_id=user),
        status="pending"
    ).exists():
        messages.info(request, "A pending request already exists.")
        return HttpResponse("A pending request already exists.")

    friend_request.objects.create(sender_id=user, receiver_id=friend, status="pending")
    messages.success(request, "Friend request sent.")
    return redirect("friends")


def friends_page(request):
    my_id = request.session.get("user_id")
    if not my_id:
        return redirect("login")

    pending_requests = friend_request.objects.filter(
        receiver_id_id=my_id, status="pending"
    ).select_related("sender_id")

    return render(request, "friends/pending_req.html", {
        "pending_requests": pending_requests
    })


@require_POST
@transaction.atomic
def respond_friend_request(request, req_id):
    """Handle approve or reject of a friend request"""
    my_id = request.session.get("user_id")
    if not my_id:
        return redirect("login")

    fr = get_object_or_404(
        friend_request,
        id=req_id,
        receiver_id_id=my_id,
        status="pending"
    )

    action = request.POST.get("action")

    if action == "accept":
        friend_list.objects.get_or_create(user_id=fr.sender_id, friend_id=fr.receiver_id)
        friend_list.objects.get_or_create(user_id=fr.receiver_id, friend_id=fr.sender_id)
        fr.status = "accepted"
        fr.save(update_fields=["status"])
        messages.success(request, f"Friend request from {fr.sender_id} accepted ✅")

    elif action == "reject":
        fr.status = "rejected"
        fr.save(update_fields=["status"])
        messages.info(request, f"Friend request from {fr.sender_id} rejected ❌")

    return redirect("friends")
