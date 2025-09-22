from django.contrib import admin
from .models import friend_list, friend_request
from comments.models import Comment

@admin.register(friend_request)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "sender_id", "receiver_id", "status", "create_at")
    list_filter = ("status", "create_at")
    search_fields = ("sender_id__fname", "receiver_id__fname", "sender_id__email", "receiver_id__email")


@admin.register(friend_list)
class FriendListAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "friend_id", "create_at")
    search_fields = ("user_id__fname", "friend_id__fname", "user_id__email", "friend_id__email")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "profile_owner", "text", "created_at")
    search_fields = ("author__fname", "author__email", "profile_owner__fname", "profile_owner__email", "text")
    list_filter = ("created_at",)
